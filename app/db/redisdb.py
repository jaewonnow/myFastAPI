import redis
from redis.exceptions import RedisError
from typing import Generator
from fastapi import Depends, HTTPException, status

# Redis 클라이언트 연결 정보
# 일반적으로 환경 변수에서 가져오는 것이 좋습니다.
# host='localhost', port=6379는 기본 설정입니다.
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# Redis 클라이언트 생성 (연결 풀 사용)
# decode_responses=True로 설정하면 Redis에서 가져온 byte 데이터를 자동으로 문자열로 변환합니다.
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    # 연결 상태를 확인하기 위해 ping을 시도합니다.
    redis_client.ping()
    print("Redis 서버와 성공적으로 연결되었습니다.")
except RedisError as e:
    print(f"Redis 연결 실패: {e}")
    redis_client = None


def get_redis_client() -> Generator[redis.Redis, None, None]:
    """
    FastAPI의 의존성 주입에 사용할 Redis 클라이언트 제너레이터 함수.
    요청마다 Redis 클라이언트를 제공하고, 요청이 끝나면 연결을 닫습니다.
    (redis-py의 기본 연결 풀링으로 인해 실제로는 풀에서 연결을 반환합니다)
    """
    if redis_client is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Redis 서버에 연결할 수 없습니다."
        )
    
    # yield를 사용하여 Redis 클라이언트를 반환하고, 요청이 끝날 때까지 유지
    try:
        yield redis_client
    finally:
        # yield를 사용하면 요청이 끝나면 이 부분이 실행됩니다.
        # redis-py의 연결 풀링 덕분에 db.close()를 호출할 필요가 없습니다.
        # 만약 풀링을 사용하지 않는다면 db.close()를 여기서 호출해야 합니다.
        pass