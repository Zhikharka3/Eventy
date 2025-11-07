// Переключатель темы
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Обновляем иконку
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        themeIcon.textContent = newTheme === 'dark' ? '🌙' : '☀️';
    }
}

// Загружаем сохраненную тему
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
    
    // Добавляем кнопку если ее нет
    if (!document.querySelector('.theme-switcher')) {
        const themeSwitcher = document.createElement('div');
        themeSwitcher.className = 'theme-switcher';
        themeSwitcher.innerHTML = `
            <button class="theme-btn" onclick="toggleTheme()">
                <span id="theme-icon">${savedTheme === 'dark' ? '🌙' : '☀️'}</span>
            </button>
        `;
        document.body.appendChild(themeSwitcher);
    }
});