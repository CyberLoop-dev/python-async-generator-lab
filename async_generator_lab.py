import argparse
import asyncio
from collections.abc import AsyncIterator


async def numbers(limit: int = 4) -> AsyncIterator[int]:
    for value in range(1, limit + 1):
        await asyncio.sleep(0)
        yield value


async def closable_stream(cleaned: list[bool]) -> AsyncIterator[str]:
    try:
        for value in ("alpha", "beta", "gamma"):
            await asyncio.sleep(0)
            yield value
    finally:
        cleaned.append(True)
        print("generator cleanup: finally block executed")


async def iterate_demo() -> None:
    print("async for:")
    async for value in numbers():
        print(" yielded", value)
    print("manual anext:")
    stream = numbers(2)
    print(" ", await anext(stream))
    print(" ", await anext(stream))
    await stream.aclose()


async def close_demo() -> None:
    cleaned: list[bool] = []
    stream = closable_stream(cleaned)
    print("first value:", await anext(stream))
    print("closing before the stream is exhausted")
    await stream.aclose()
    print("cleanup observed:", bool(cleaned))


async def run(scenario: str) -> None:
    if scenario in ("iterate", "all"):
        await iterate_demo()
    if scenario in ("close", "all"):
        await close_demo()


def main() -> None:
    parser = argparse.ArgumentParser(description="Explore Python async generator behavior.")
    parser.add_argument("--scenario", choices=("iterate", "close", "all"), default="all")
    args = parser.parse_args()
    asyncio.run(run(args.scenario))


if __name__ == "__main__":
    main()
