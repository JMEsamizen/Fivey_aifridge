const notificationButton = document.getElementById("enableNotifications");
const expiryReminders = document.querySelectorAll(".expiry-reminder");

function showBrowserReminders() {
    if (!("Notification" in window) || Notification.permission !== "granted") {
        return;
    }

    expiryReminders.forEach((reminder) => {
        const storageKey = `fivey-expiry-reminder-${reminder.dataset.notificationId}`;
        if (localStorage.getItem(storageKey)) {
            return;
        }

        const notification = new Notification(reminder.dataset.notificationTitle, {
            body: reminder.dataset.notificationMessage,
        });
        notification.onclick = () => {
            window.focus();
            window.location.href = reminder.href;
        };
        localStorage.setItem(storageKey, "shown");
    });
}

if (notificationButton) {
    if (!("Notification" in window)) {
        notificationButton.hidden = true;
    } else if (Notification.permission === "granted") {
        notificationButton.textContent = "Browser reminders enabled";
        showBrowserReminders();
    } else if (Notification.permission === "denied") {
        notificationButton.hidden = true;
    } else {
        notificationButton.addEventListener("click", async () => {
            const permission = await Notification.requestPermission();
            if (permission === "granted") {
                notificationButton.textContent = "Browser reminders enabled";
                showBrowserReminders();
            }
        });
    }
}
