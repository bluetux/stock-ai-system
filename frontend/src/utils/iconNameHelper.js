// src/utils/iconNameHelper.js
export const toPascalCase = (str) =>
    str
      .split(/[-_]/g)
      .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
      .join("");