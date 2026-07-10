import pytest
import time


@pytest.fixture(autouse=True)
def execute_time():
    start = time.time()
    yield
    end = time.time()
    print(f"\nТесты выполнился за: {(end - start):.2f} сек.\n")
