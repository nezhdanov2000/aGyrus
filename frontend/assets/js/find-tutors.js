(function(){
    const API_BASE = '/backend/api/';
    let searchInput, searchBtn, results;

    async function init(){
        searchInput = document.getElementById('searchInput');
        searchBtn = document.getElementById('searchBtn');
        results = document.getElementById('results');

        if (window.PopupMenu) new PopupMenu();

        searchBtn.addEventListener('click', runSearch);
        searchInput.addEventListener('keydown', (e)=>{ if(e.key==='Enter') runSearch(); });

        // initial demo query from mockup
        if (searchInput.value.trim()==='') searchInput.value = 'Walter';
        runSearch();
    }

    async function runSearch(){
        const q = searchInput.value.trim();
        results.innerHTML = '';
        if(!q){ return; }
        try{
            const res = await fetch(`${API_BASE}search-tutors.php`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: q })
            });
            const data = await res.json();
            if(!data.success){
                results.textContent = data.error || 'Search failed';
                return;
            }
            renderTutors(data.tutors || []);
        }catch(err){
            results.textContent = 'Network error';
        }
    }

    function renderTutors(tutors){
        if(tutors.length===0){
            results.textContent = 'No tutors found';
            return;
        }
        tutors.forEach(t => {
            const card = document.createElement('div');
            card.className = 'card';
            const name = `${t.name} ${t.surname}`.trim();
            const photo = t.photo_link || '../assets/images/logo.png';
            const courses = (t.courses || '').split(',').map(s=>s.trim()).filter(Boolean).join(', ');
            card.innerHTML = `
                <img src="${photo}" alt="${name}">
                <div>
                    <h3>${name}</h3>
                    <p>${courses || '—'}</p>
                    <div class="actions">
                        <button class="btn primary" data-id="${t.tutor_id}">choose</button>
                    </div>
                </div>
            `;
            card.querySelector('.btn.primary').addEventListener('click', ()=>{
                window.location.href = `./tutor-calendar.html?tutor_id=${t.tutor_id}`;
            });
            results.appendChild(card);
        });
    }

    document.addEventListener('DOMContentLoaded', init);
})();


