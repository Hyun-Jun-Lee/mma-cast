-- 사용자 생성
CREATE USER mma_cast WITH ENCRYPTED PASSWORD 'mma_cast';

-- 데이터베이스 생성
CREATE DATABASE airflow;
CREATE DATABASE mma_cast;

-- 데이터베이스에 대한 권한 부여
GRANT ALL PRIVILEGES ON DATABASE airflow TO mma_cast;
GRANT ALL PRIVILEGES ON DATABASE mma_cast TO mma_cast;