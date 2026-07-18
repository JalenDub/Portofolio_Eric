document.addEventListener('DOMContentLoaded', () => {
    
    const tabButtons = document.querySelectorAll('.nav-tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');

            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            tabContents.forEach(content => content.classList.remove('active'));
            
            const targetContent = document.getElementById(`tab-${targetTab}`);
            if (targetContent) {
                targetContent.classList.add('active');
            }

            const newUrl = new URL(window.location);
            newUrl.searchParams.set('tab', targetTab);
            window.history.pushState({}, '', newUrl);
        });
    });

    const modals = document.querySelectorAll('.modal');
    const closeButtons = document.querySelectorAll('.modal-close');

    closeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            modals.forEach(modal => modal.classList.remove('active'));
        });
    });

    window.addEventListener('click', (e) => {
        modals.forEach(modal => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });

    const editSkillButtons = document.querySelectorAll('.edit-skill-btn');
    const modalSkill = document.getElementById('modal-skill');
    const formEditSkill = document.getElementById('form-edit-skill');

    editSkillButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            const nama = btn.getAttribute('data-nama');
            const kategori = btn.getAttribute('data-kategori');
            const persentase = btn.getAttribute('data-persentase');

            document.getElementById('edit_nama_skill').value = nama;
            document.getElementById('edit_kategori').value = kategori;
            document.getElementById('edit_persentase').value = persentase;

            formEditSkill.action = `/admin/skills/edit/${id}`;

            modalSkill.classList.add('active');
        });
    });

    const editPengalamanButtons = document.querySelectorAll('.edit-pengalaman-btn');
    const modalPengalaman = document.getElementById('modal-pengalaman');
    const formEditPengalaman = document.getElementById('form-edit-pengalaman');

    editPengalamanButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            const perusahaan = btn.getAttribute('data-perusahaan');
            const posisi = btn.getAttribute('data-posisi');
            const mulai = btn.getAttribute('data-mulai');
            const selesai = btn.getAttribute('data-selesai');
            const deskripsi = btn.getAttribute('data-deskripsi');

            document.getElementById('edit_perusahaan').value = perusahaan;
            document.getElementById('edit_posisi').value = posisi;
            document.getElementById('edit_tanggal_mulai').value = mulai;
            document.getElementById('edit_tanggal_selesai').value = selesai;
            document.getElementById('edit_deskripsi_pengalaman').value = deskripsi;

            formEditPengalaman.action = `/admin/pengalaman/edit/${id}`;

            modalPengalaman.classList.add('active');
        });
    });

    const editProyekButtons = document.querySelectorAll('.edit-proyek-btn');
    const modalProyek = document.getElementById('modal-proyek');
    const formEditProyek = document.getElementById('form-edit-proyek');

    editProyekButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            const judul = btn.getAttribute('data-judul');
            const teknologi = btn.getAttribute('data-teknologi');
            const linkproyek = btn.getAttribute('data-linkproyek');
            const linkgithub = btn.getAttribute('data-linkgithub');
            const deskripsi = btn.getAttribute('data-deskripsi');

            document.getElementById('edit_judul').value = judul;
            document.getElementById('edit_teknologi').value = teknologi;
            document.getElementById('edit_link_proyek').value = linkproyek;
            document.getElementById('edit_link_github').value = linkgithub;
            document.getElementById('edit_deskripsi_proyek').value = deskripsi;

            formEditProyek.action = `/admin/proyek/edit/${id}`;

            modalProyek.classList.add('active');
        });
    });
});
