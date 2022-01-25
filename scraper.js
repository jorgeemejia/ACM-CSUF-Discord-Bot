const formatTime = (str) => {
	if (str.includes("TBA")) return '00:00:00'
    let times = str.substr(0, 5).split(":")
	let hours = parseInt(times[0])
    let minutes = times[1].replace("p", "")
    if (str.includes("pm") && hours > 12) hours += 12
    return `${String(hours).padStart(2, '0')}:${minutes}:00`
}

let str = ""

const get = (p, selector) => { return p.querySelector(selector).textContent.trim().replace('\'', '\\\'') }

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
    const location = get(back1, ".building").split('/').slice(0, 2).join('/')
    const id = get(back2, ".crn").split(" ")[1]
    const days = get(back1, ".days").split('/').slice(0, 2).join('/')
    str += `INSERT INTO CLASS VALUES (${id}, '${subject}', '${number}', '${section}', '${title}', '2022', 'SPRING', '${instructor}', '${location}', '${startTime}', '${endTime}', '${days}');\n`
})
console.log(str)

