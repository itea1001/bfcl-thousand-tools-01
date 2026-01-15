# Prompt Variation Integration Status

## Goal
Test whether format sensitivity changes as the number of distractor functions increases (i.e., does the model become more/less sensitive to prompt format when dealing with larger function pools?).

## Completed
1. ✅ **Copied prompt_variations.py** from `bfcl-pv-01` project
   - Contains all format instructions (JSON, XML, Python, Tagged variants)
   - Located at: `berkeley-function-call-leaderboard/bfcl_eval/constants/prompt_variations.py`

2. ✅ **Added CLI flags**
   - `--prompt-variation` flag added to both `generate` and `evaluate` commands
   - Example usage: `--prompt-variation "res_fmt=json,doc_fmt=json"`
   - Can be verified with: `python -m bfcl_eval generate --help`

3. ✅ **Created test file symlinks**
   - Symlinked pool 128 and 512 test files to BFCL data directory
   - Files: `BFCL_v4_simple_python_pool128.json`, `BFCL_v4_simple_python_pool512.json`

4. ✅ **Created experiment runner script**
   - Script: `scripts/run_prompt_variation_experiments.py`
   - Configured to test 3 formats × 3 pool sizes (baseline, 128, 512)

5. ✅ **Basic infrastructure**
   - Placeholder code in `_llm_response_generation.py` main function
   - Git commits pushed to repo

## Still Needed
1. ❌ **Wire variation logic into model handlers**
   - Modify how system prompts are constructed in BaseHandler
   - Apply the appropriate format instruction based on `prompt_variation` arg
   - Currently the flag is recognized but not acted upon

2. ❌ **Add parsers for non-JSON formats**
   - XML parser
   - Python parser
   - Tagged format parser
   - Currently only JSON parsing is supported

3. ❌ **Integration testing**
   - Test that each format works end-to-end
   - Verify evaluation correctly handles different output formats

## Next Steps (Pending Decision)
**Option 1**: Full integration
- Complete the model handler modifications
- Add all necessary parsers
- Run full experiment suite
- Time estimate: Several hours

**Option 2**: Minimal viable test
- Manually modify system prompts for a few test cases
- Run limited experiments to validate the approach
- Document findings and defer full automation

**Option 3**: Defer to later
- Document current state
- Focus on other project deliverables
- Return to this when time permits

## Files Modified
- `berkeley-function-call-leaderboard/bfcl_eval/__main__.py`
- `berkeley-function-call-leaderboard/bfcl_eval/_llm_response_generation.py`
- `berkeley-function-call-leaderboard/bfcl_eval/constants/prompt_variations.py` (new)
- `scripts/run_prompt_variation_experiments.py` (new)

