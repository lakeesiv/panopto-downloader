const getArray = () => {
  let performance =
    window.performance ||
    window.msPerformance ||
    window.webkitPerformance ||
    {};
  let network = performance.getEntries() || {};

  let names = network.map((n) => n.name);
  return names.filter((n) => n.includes(".m3u8") && !n.includes("index"));
};

const pressCamera = () => {
  document.querySelector("[aria-pressed=false]").click();
};

let a = getArray();
pressCamera();
let b = getArray();
let c = a.concat(b.filter((item) => a.indexOf(item) < 0));
return Array.from(new Set(a.concat(b)));
