const formatTime = (str) => {
	if (str == "TBA") return '00:00:00'
    let hours = 0
    if (str.includes("pm")) hours = 12
    str = str.substr(0, 4)
    times = str.split(":")
    times = [parseInt(times[0]), parseInt(times[1])]
    hours += times[0]
    let minutes = times[1]
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:00`
}

let str = ""

const get = (p, selector) => { return p.querySelector(selector).textContent.trim() }

document.querySelectorAll("#cardContainer div.wrap").forEach((c) => {
	back1 = c.querySelector("div.card.back")
	back2 = c.querySelector("div.card.back2")
    const subject = get(back1, ".subject")
    const number = get(back1, ".number")
    const section = get(back1, ".section")
    const times = get(back1, ".time").split('-')
    const startTime = formatTime(times[0])
    const endTime = formatTime(times[1])
    const instructor = get(back1, ".instructor")
    const title = get(back1, ".abbrevTitle")
    const location = get(back1, ".building")
    const id = get(back2, ".crn").split(" ")[1]
    str += `INSERT INTO CLASS VALUES (${id}, '${subject}', '${number}', '${section}', '${title}', '2022', 'SPRING', '${instructor}', '${location}', '${startTime}', '${endTime}');\n`
})
console.log(str)
