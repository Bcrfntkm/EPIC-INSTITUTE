// 1. FizzBuzz without if, switch, or ternary operator
function fizzBuzz() {
        const map = { 3: "Fizz", 5: "Buzz" };
    for (let i = 1; i <= 100; i++) {
      console.log((map[3 * !(i % 3)] || "") + (map[5 * !(i % 5)] || "") || i);
    }
  }
  
  // 2. Palindrome checker
  function isPalindrom(str) {
    return str === str.split('').reverse().join('');
  }
  
  // 3. Draw Calendar
  function drawCalendar(year, month) {
    let date = new Date(year, month - 1, 1);
    let result = 'Calendar for ${month}/${year}\n';
    result += 'Mo Tu We Th Fr Sa Su\n';
    let firstDay = date.getDay() || 7;
    result += '   '.repeat(firstDay - 1);
    while (date.getMonth() === month - 1) {
      result += date.getDate().toString().padStart(2, ' ') + ' ';
      if (date.getDay() === 0) result += '\n';
      date.setDate(date.getDate() + 1);
    }
    return result;
  }
  
  // 4. Deep Equality
  function isDeepEqual(a, b) {
    return JSON.stringify(a) === JSON.stringify(b);
  }
  
  // 5. Spiral traversal
  function spiral(matrix) {
    let result = [];
    while (matrix.length) {
      result.push(...matrix.shift());
      matrix = matrix[0] ? matrix.map(row => row.pop()).filter(x => x !== undefined) : [];
      matrix.reverse();
      matrix = matrix.map(row => row.reverse());
    }
    return result;
  }
  
  // 6. Quadratic Equation solver
  function quadraticEquation(a, b, c) {
    let d = b * b - 4 * a * c;
    if (d < 0) return [];
    if (d === 0) return [-b / (2 * a)];
    return [(-b + Math.sqrt(d)) / (2 * a), (-b - Math.sqrt(d)) / (2 * a)];
  }
