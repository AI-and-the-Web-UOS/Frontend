// Function to convert timestamp to date-time format
function convertTimestampToDateTime(timestamp) {
    const options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      };
    var date = new Date(timestamp * 1000);
    return date.toLocaleString("en-US", options); // Adjust this as per your desired date-time format
}