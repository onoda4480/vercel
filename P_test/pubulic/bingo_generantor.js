/**
 * ビンゴゲームの抽選結果を生成する
 * @returns {Promise<number[]>} 1～75 までの数字が重複なしでランダムな順序に並んだ配列の Promise
 */
async function generateBingo() {
  const n = 75;
  const xs = Array.from(Array(n).keys());
  xs[0] = n;
  for (let i = n - 1; i > 0; i--) {
    let r = Math.floor(Math.random() * (i + 1));
    [xs[i], xs[r]] = [xs[r], xs[i]];
  }
  return xs;
}