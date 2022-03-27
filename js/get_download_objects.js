const getObject = (element) => {
  try {
    const link = element.getElementsByClassName("aalink")[0].href;
    const splitText = element
      .getElementsByClassName("instancename")[0]
      .innerText.split(/\r?\n/);
    const type = splitText[splitText.length - 1];
    const text = splitText[0];
    if (type === "File") {
      return { link, text };
    }
  } catch (error) {
    return null;
  }
};

const filterBySubstrings = (
  data,
  validSubstrings,
  invalidSubstrings = undefined
) =>
  data.filter(({ text }) => {
    const condition1 = validSubstrings.some((substring) =>
      text.includes(substring)
    );
    if (invalidSubstrings) {
      const condition2 = !invalidSubstrings.some((substring) =>
        text.includes(substring)
      );
      return condition1 && condition2;
    }
    return condition1;
  });

const getPDFObjects = (validSubstrings, invalidSubstrings = undefined) => {
  const elements = document.getElementsByClassName("activityinstance");
  const res = Array.from(elements).reduce((arr, element) => {
    const object = getObject(element);
    if (object) {
      arr.push(object);
    }
    return arr;
  }, []);

  return filterBySubstrings(res, validSubstrings, invalidSubstrings);
};

res = getPDFObjects(["pdf"]);
console.log(res);
