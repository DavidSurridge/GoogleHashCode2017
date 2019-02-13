const HIGHEST_SCORE = require('../lib/highest_score');

const { copySolution, formatTime } = require('../lib/helpers');

const CONSTS = require('../lib/consts');

// Hill climbing
// - Create initial solution
// - Loop
//   - Try NB_VARIANTS different variants
//   - Loop until none of these variants give a better score
//
// - Try the above NB_RUNS times and keep the best solution

const apply = (input, initialSolutionFn, createVariantFn) => {
  const consts = CONSTS[input.filename] || CONSTS.default; 

  console.log(`FILE_SIZE = ${input.filesize}  /  NB_RUNS = ${consts.NB_RUNS}  /  NB_VARIANTS = ${consts.NB_VARIANTS} / HIGHEST_SCORE = ${HIGHEST_SCORE[input.filename]}\n`);

  let bestSolution = { score: 0 };
  for (let runId = 0; runId < consts.NB_RUNS; runId++) {
    let solution = {
      cacheServers: {},
      requests: []
    };

    // Initial random solution
    initialSolutionFn(solution, input);

    // Try new solutions
    let isVariantBetter = false;
    do {
      let bestVariantScore = 0;
      let bestVariant = undefined;
      for (let variantId = 0; variantId < consts.NB_VARIANTS; variantId++) {
        const variantSolution = copySolution(solution);
        
        createVariantFn(variantSolution, input);
   
        if (variantSolution.score > bestVariantScore) {
          bestVariantScore = variantSolution.score;
          bestVariant = variantSolution;
        }
      }
      if (bestVariantScore > solution.score) {
        solution = copySolution(bestVariant);
        isVariantBetter = true;
        console.log(`${bestVariantScore} / ${HIGHEST_SCORE[input.filename]}`);
      } else {
        isVariantBetter = false;
      }
    } while (isVariantBetter);
    // Exit loop when not getting better scores


    // Compare to previous best solution
    if (solution.score > bestSolution.score) {
      bestSolution = solution;
      console.log(`Run #${runId}`);
      console.log(bestSolution.score);
    }
  }
  input.solution = bestSolution;
};

module.exports = {
  apply
};