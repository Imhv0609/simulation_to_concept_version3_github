#!/usr/bin/env python3
"""Show what agent's system prompt now contains"""
import sys
sys.path.insert(0, '.')

from simulations_config import get_simulation

sim_config = get_simulation('brackets_signs')

# Build problem examples string (same as in teacher.py)
problem_examples_str = ''
if 'problem_examples' in sim_config:
    examples = sim_config['problem_examples']
    problem_examples_str = '\n\nAVAILABLE EXAMPLES (problemIndex):\n'
    for ex in examples:
        rule_emoji = '➖' if ex['rule'] == 'minus' else '➕'
        problem_examples_str += f"{rule_emoji} {ex['index']}: {ex['expression']} = {ex['result'].split('=')[0].strip()} ({ex['rule'].upper()} before bracket)\n"
    problem_examples_str += '\n⚠️ CRITICAL: Always check this list to know which problemIndex shows which rule!'

print('AGENT SYSTEM PROMPT NOW INCLUDES:')
print('='*70)
print(problem_examples_str)
print()
print('With this information, the agent will:')
print('✅ Know that problemIndex=2 shows MINUS before bracket')
print('✅ Know that problemIndex=3 shows PLUS before bracket')
print('✅ Make accurate statements about sign rules')
