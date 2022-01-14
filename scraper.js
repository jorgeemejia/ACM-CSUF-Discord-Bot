let str = ""

const get = (p, selector) => return p.querySelector(selector).textContent.trim()	

document.querySelectorAll("#cardContainer div.wrap > div.card.back").forEach((c) => {
    const subject = get(".subject")
    const number = get(".number")
    const section = get(".section")
    const time = get(".time")
    const instructor = get(".instructor")
    const title = get(".abbrevTitle")
    str += `"${subject}${number}-${section}": {"time": "${time}", "instructor": "${instructor}", "title": "${title}" },\n`
})
console.log(str)
