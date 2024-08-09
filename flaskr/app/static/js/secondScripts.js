// function displayDateTime() {
//     const now = new Date();
//     const dateTimeString = now.toLocaleString();
//     document.getElementById('dateTime').innerText = dateTimeString;
// }

// // Call the function when the page loads
// window.onload = displayDateTime;

// // Update the date and time every second
// setInterval(displayDateTime, 1000);
// function displayDate() {
//     const now = new Date();

//     // Get the full weekday and day
//     const options = { weekday: 'long', day: 'numeric' };
//     const dayAndWeekday = now.toLocaleDateString(undefined, options);

//     // Get the full month name and abbreviate it manually
//     const fullMonth = now.toLocaleString(undefined, { month: 'long' });
//     const shortMonth = fullMonth.slice(0, 3);

//     // Get the year
//     const year = now.getFullYear();

//     // Combine all parts
//     const dateString = `${dayAndWeekday}, ${shortMonth} ${year}`;

//     document.getElementById('date').innerText = dateString;
// }

// // Call the function when the page loads

   function displayDate() {
            const now = new Date();

            // Get the full weekday and day
            const options = { weekday: 'short', day: 'numeric' };
            const dayAndWeekday = now.toLocaleDateString(undefined, options);

            // Abbreviate the month manually
            const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
            const shortMonth = months[now.getMonth()];

            // Get the year
            const year = now.getFullYear();

            // Combine all parts
            const dateString = `${dayAndWeekday}, ${shortMonth} ${year}`;

            document.getElementById('date').innerText = dateString;

            document.getElementById('date1').innerText = dateString;
        }

        // Call the function when the page loads
        window.onload = displayDate;

     
    