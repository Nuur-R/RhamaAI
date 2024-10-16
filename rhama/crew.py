#!/usr/bin/env python
import asyncio
from crew_pipelines import pipeline as pl

async def run():
    """
    Run the pipeline.
    """
    inputs = [
        {"topic": "Youg age diabetes in Indonesia"},
    ]
    pipeline = pl.RhamaPipeline()
    results = await pipeline.kickoff(inputs)
    
    # Process and print results
    for result in results:
        print(f"Raw output: {result.raw}")
        if result.json_dict:
            print(f"JSON output: {result.json_dict}")
        print("\n")

def main():
    asyncio.run(run())

if __name__ == "__main__":
    main()