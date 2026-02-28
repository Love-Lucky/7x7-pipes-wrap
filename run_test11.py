#!/usr/bin/env python3
"""Chạy test11 và lưu kết quả vào output/test11_result.txt"""
import tracemalloc
import time
from main import PipeState, astar, count_open_ends

with open('test_inputs/test11_medium_five.txt', 'r') as f:
    puzzle_str = f.read()

tracemalloc.start()
start = time.time()
state = PipeState.from_string(puzzle_str)
open_ends_initial = count_open_ends(state)

output = []
output.append("="*80)
output.append("TEST CASE: test11_medium_five.txt")
output.append("="*80)
output.append("")
output.append("INITIAL STATE:")
output.append("-" * 9)
for row in state.grid:
    output.append("|" + "".join(tile.to_char() for tile in row) + "|")
output.append("-" * 9)
output.append(f"\nOpen ends: {open_ends_initial}")
output.append("Difficulty: MEDIUM")
output.append("")
output.append("-"*80)
output.append("RUNNING A* SEARCH...")
output.append("-"*80)
output.append("")

solution, path, stats = astar(state, show_progress=False)

elapsed = time.time() - start
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

output.append("="*80)
output.append("RESULT")
output.append("="*80)
output.append("")

if solution:
    open_ends_final = count_open_ends(solution)
    peak_mb = peak / 1024 / 1024
    output.append("Status: SOLVED ✅")
    output.append("")
    output.append("Performance Metrics:")
    output.append(f"  - Time: {elapsed:.3f} seconds")
    output.append(f"  - RAM Peak: {peak_mb:.2f} MB")
    output.append(f"  - Nodes explored: {stats['nodes_explored']:,}")
    output.append(f"  - Path length: {len(path)} steps")
    output.append(f"  - Avg nodes/sec: {stats['nodes_explored']/elapsed:,.0f}")
    output.append("")
    output.append("FINAL STATE (SOLVED):")
    output.append("-" * 9)
    for row in solution.grid:
        output.append("|" + "".join(tile.to_char() for tile in row) + "|")
    output.append("-" * 9)
    output.append(f"\nFinal open ends: {open_ends_final}")
else:
    output.append("Status: NOT SOLVED ❌")
    output.append(f"Nodes explored: {stats['nodes_explored']:,}")

output.append("="*80)
text = "\n".join(output)
print(text)
with open('output/test11_result.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("\n\n✅ Đã lưu kết quả vào: output/test11_result.txt")
