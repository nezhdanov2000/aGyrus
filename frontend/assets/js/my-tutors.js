(function(){
    const API_BASE = window.CONFIG ? window.CONFIG.API_BASE : '/backend/api/';
    let listEl, floatingEl, closeFloatingBtn, notifyBtn, cancelAllBtn;
    let tutors = [];

    async function init(){
        listEl = document.getElementById('list');
        floatingEl = document.getElementById('floating-panel');
        closeFloatingBtn = document.getElementById('closeFloating');
        notifyBtn = document.getElementById('notifyBtn');
        cancelAllBtn = document.getElementById('cancelAllBtn');
        if (window.PopupMenu) new PopupMenu();

        closeFloatingBtn.addEventListener('click', ()=> floatingEl.classList.add('hidden'));

        await loadTutors();
        render();

        // Example actions (stubs)
        notifyBtn.addEventListener('click', ()=>{ alert('Notification sent to tutors'); floatingEl.classList.add('hidden'); });
        cancelAllBtn.addEventListener('click', async ()=>{
            // Cancel all bookings for all tutors
            const bookings = await fetchMyBookings();
            for (const b of bookings){
                await fetch(`${API_BASE}booking/cancel-booking.php`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ booking_id: b.booking_id })});
            }
            await loadTutors();
            render();
            floatingEl.classList.add('hidden');
        });
    }

    async function fetchMyBookings(){
        try{
            const res = await fetch(`${API_BASE}booking/my-bookings.php`);
            const data = await res.json();
            if (data && data.success) return data.bookings || [];
        }catch(e){}
        return [];
    }

    async function loadTutors(){
        const bookings = await fetchMyBookings();
        const map = new Map();
        for (const b of bookings){
            const id = Number(b.tutor_id);
            if(!map.has(id)){
                map.set(id, { tutor_id:id, name: b.tutor_name, photo_link: b.photo_link, count:0 });
            }
            map.get(id).count += 1;
        }
        tutors = Array.from(map.values());
    }

    function render(){
        listEl.innerHTML = '';
        if (tutors.length === 0){
            listEl.textContent = 'You have no tutors yet';
            return;
        }
        tutors.forEach(t => listEl.appendChild(renderCard(t)));
    }

    function renderCard(t){
        const el = document.createElement('div');
        el.className = 'card';
        const photo = t.photo_link || '../assets/images/logo.png';
        const name = t.name;
        el.innerHTML = `
            <img src="${photo}" alt="${name}">
            <div>
                <h3>${name}</h3>
                <div class="row">
                    <button class="btn primary">check timelots</button>
                </div>
                <div class="row" style="margin-top:10px;">
                    <button class="icon small">✉️</button>
                    <button class="icon small danger">✖️</button>
                </div>
            </div>
        `;
        el.querySelector('.btn.primary').addEventListener('click', ()=>{
            window.location.href = `./tutor-calendar.html?tutor_id=${t.tutor_id}`;
        });
        const [mailBtn, delBtn] = el.querySelectorAll('.icon.small');
        mailBtn.addEventListener('click', ()=> floatingEl.classList.remove('hidden'));
        delBtn.addEventListener('click', async ()=>{
            if(!confirm('Cancel all your bookings with this tutor?')) return;
            const bookings = await fetchMyBookings();
            const mine = bookings.filter(b => Number(b.tutor_id) === Number(t.tutor_id));
            for (const b of mine){
                await fetch(`${API_BASE}booking/cancel-booking.php`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ booking_id: b.booking_id })});
            }
            await loadTutors();
            render();
        });
        return el;
    }

    document.addEventListener('DOMContentLoaded', init);
})();


