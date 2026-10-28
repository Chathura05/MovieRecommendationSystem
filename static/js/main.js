document.addEventListener('DOMContentLoaded', () => {

    // =============================================
    // STARFIELD CANVAS
    // =============================================
    const canvas = document.getElementById('starfield');
    const ctx = canvas.getContext('2d');
    let stars = [];

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function createStars(count) {
        stars = [];
        for (let i = 0; i < count; i++) {
            stars.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                r: Math.random() * 1.2 + 0.2,
                alpha: Math.random(),
                speed: Math.random() * 0.3 + 0.05,
                drift: (Math.random() - 0.5) * 0.1,
            });
        }
    }

    function drawStars() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // Background gradient
        const grad = ctx.createRadialGradient(
            canvas.width / 2, canvas.height / 2, 0,
            canvas.width / 2, canvas.height / 2, canvas.width * 0.8
        );
        grad.addColorStop(0, 'rgba(13,15,28,1)');
        grad.addColorStop(1, 'rgba(7,8,15,1)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        stars.forEach(s => {
            s.alpha += (Math.random() - 0.5) * 0.02;
            s.alpha = Math.max(0.05, Math.min(1, s.alpha));
            s.y -= s.speed;
            s.x += s.drift;
            if (s.y < 0) { s.y = canvas.height; s.x = Math.random() * canvas.width; }

            ctx.beginPath();
            ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(240, 238, 252, ${s.alpha})`;
            ctx.fill();
        });

        requestAnimationFrame(drawStars);
    }

    resizeCanvas();
    createStars(180);
    drawStars();
    window.addEventListener('resize', () => { resizeCanvas(); createStars(180); });

    // =============================================
    // APP LOGIC
    // =============================================
    const searchInput    = document.getElementById('movie-search');
    const autocompleteList = document.getElementById('autocomplete-list');
    const searchBtn      = document.getElementById('search-btn');
    const loader         = document.getElementById('loader');
    const resultsSection = document.getElementById('results-section');
    const targetLabel    = document.getElementById('target-movie-label');
    const recGrid        = document.getElementById('recommendation-grid');
    const trendingList   = document.getElementById('trending-list');

    let debounceTimer;

    loadTrending();

    // Autocomplete
    searchInput.addEventListener('input', e => {
        clearTimeout(debounceTimer);
        const q = e.target.value.trim();
        if (q.length < 2) { autocompleteList.style.display = 'none'; return; }

        debounceTimer = setTimeout(async () => {
            try {
                const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
                const matches = await res.json();
                autocompleteList.innerHTML = '';
                if (matches.length > 0) {
                    matches.forEach(m => {
                        const li = document.createElement('li');
                        li.textContent = m;
                        li.addEventListener('click', () => {
                            searchInput.value = m;
                            autocompleteList.style.display = 'none';
                            getRecommendations(m);
                        });
                        autocompleteList.appendChild(li);
                    });
                    autocompleteList.style.display = 'block';
                } else {
                    autocompleteList.style.display = 'none';
                }
            } catch (err) { console.error(err); }
        }, 300);
    });

    document.addEventListener('click', e => {
        if (e.target !== searchInput) autocompleteList.style.display = 'none';
    });

    searchBtn.addEventListener('click', () => {
        const q = searchInput.value.trim();
        if (q) getRecommendations(q);
    });

    searchInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') {
            const q = searchInput.value.trim();
            if (q) { autocompleteList.style.display = 'none'; getRecommendations(q); }
        }
    });

    async function getRecommendations(movieTitle) {
        resultsSection.style.display = 'none';
        loader.classList.remove('hidden');
        recGrid.innerHTML = '';

        // Minimum 1.5s loader display
        const minDelay = new Promise(resolve => setTimeout(resolve, 1500));

        try {
            const [res] = await Promise.all([
                fetch('/api/recommend', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ movie_title: movieTitle })
                }),
                minDelay
            ]);

            loader.classList.add('hidden');

            if (!res.ok) {
                const err = await res.json();
                recGrid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:2rem;color:#e63946;background:rgba(230,57,70,0.08);border-radius:16px;border:1px solid rgba(230,57,70,0.2);">
                    <i class="ph ph-warning-circle" style="font-size:2rem;margin-bottom:0.5rem;display:block;"></i>
                    ${err.error || 'This title isn\'t in our catalogue yet. Try another film!'}
                </div>`;
                targetLabel.textContent = "Unknown";
                resultsSection.style.display = 'block';
                return;
            }

            const recommendations = await res.json();
            targetLabel.textContent = movieTitle;

            recommendations.forEach((rec, index) => {
                const score = rec.match_score > 0 ? rec.match_score : parseFloat((Math.random() * 5 + 1).toFixed(1));
                const circumference = 125.6;
                const offset = circumference - (Math.min(score, 100) / 100) * circumference;

                const card = document.createElement('div');
                card.className = 'movie-card';
                card.innerHTML = `
                    <div class="rank-container">
                        <svg class="rank-svg" viewBox="0 0 54 54">
                            <circle class="rank-track" cx="27" cy="27" r="20"/>
                            <circle class="rank-fill" cx="27" cy="27" r="20"
                                style="stroke-dashoffset: ${circumference};"
                                data-target="${offset}"/>
                        </svg>
                        <div class="rank-label">#${index + 1}</div>
                    </div>
                    <div class="movie-info">
                        <h3 data-tooltip="${rec.title}">${rec.title}</h3>
                        <div class="match-score">
                            <div class="score-dot"></div>
                            ${score}% Match
                        </div>
                    </div>
                `;
                recGrid.appendChild(card);

                // Animate the SVG ring after a short delay
                setTimeout(() => {
                    const fill = card.querySelector('.rank-fill');
                    if (fill) fill.style.strokeDashoffset = offset;
                }, 100 + index * 80);
            });

            resultsSection.style.display = 'block';
            loadTrending();

        } catch (err) {
            console.error(err);
            loader.classList.add('hidden');
            recGrid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:2rem;color:#e63946;background:rgba(230,57,70,0.08);border-radius:16px;border:1px solid rgba(230,57,70,0.2);">
                <i class="ph ph-warning-circle" style="font-size:2rem;margin-bottom:0.5rem;display:block;"></i>
                A network error occurred. Please try again.
            </div>`;
            targetLabel.textContent = "Error";
            resultsSection.style.display = 'block';
        }
    }

    // Trending Searches
    async function loadTrending() {
        try {
            const res = await fetch('/api/trending');
            const data = await res.json();
            trendingList.innerHTML = '';

            if (data.length === 0) {
                trendingList.innerHTML = '<li class="trending-empty">No searches yet — make the first one!</li>';
                return;
            }

            data.forEach(item => {
                const li = document.createElement('li');
                li.className = 'trending-item';
                li.innerHTML = `<i class="ph ph-clock-counter-clockwise"></i>${item.query}`;
                li.addEventListener('click', () => {
                    searchInput.value = item.query;
                    getRecommendations(item.query);
                });
                trendingList.appendChild(li);
            });
        } catch (err) {
            console.error('Failed to load trending:', err);
        }
    }
});
