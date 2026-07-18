document.addEventListener('DOMContentLoaded', () => {

    const preloader = document.getElementById('preloader');
    const pageContent = document.getElementById('pageContent');

    function hidePreloader() {
        if (preloader) {
            preloader.classList.add('loaded');
        }
        if (pageContent) {
            pageContent.classList.add('visible');
        }
        setTimeout(() => {
            initHeroTextAnimation();
            initTypewriter();
        }, 700);
    }

    window.addEventListener('load', () => {
        setTimeout(hidePreloader, 2200);
    });
    setTimeout(hidePreloader, 3500);


    const canvas = document.getElementById('particleCanvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let particles = [];
        let mouseX = 0;
        let mouseY = 0;
        let animFrameId;

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        class Particle {
            constructor() {
                this.reset();
            }

            reset() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 0.5;
                
                const isYoru = document.body.classList.contains('yoru-mode');
                const speedMultiplier = isYoru ? 1.6 : 1.0;
                this.speedX = (Math.random() - 0.5) * 0.5 * speedMultiplier;
                this.speedY = (Math.random() - 0.5) * 0.5 * speedMultiplier;
                
                this.opacity = Math.random() * 0.5 + 0.1;
                
                if (isYoru) {
                    this.color = Math.random() > 0.5
                        ? `rgba(0, 243, 255, ${this.opacity})` // Yoru Cyan
                        : `rgba(255, 91, 0, ${this.opacity})`;  // Yoru Orange
                } else {
                    this.color = Math.random() > 0.7
                        ? `rgba(255, 70, 85, ${this.opacity})`
                        : `rgba(236, 232, 225, ${this.opacity * 0.5})`;
                }
            }

            update() {
                this.x += this.speedX;
                this.y += this.speedY;

                const dx = this.x - mouseX;
                const dy = this.y - mouseY;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 120) {
                    const force = (120 - dist) / 120;
                    this.x += (dx / dist) * force * 0.8;
                    this.y += (dy / dist) * force * 0.8;
                }

                if (this.x < 0) this.x = canvas.width;
                if (this.x > canvas.width) this.x = 0;
                if (this.y < 0) this.y = canvas.height;
                if (this.y > canvas.height) this.y = 0;
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.fill();
            }
        }

        function updateParticleThemes() {
            const isYoru = document.body.classList.contains('yoru-mode');
            particles.forEach(p => {
                p.opacity = Math.random() * 0.5 + 0.1;
                const speedMultiplier = isYoru ? 1.6 : 1.0;
                p.speedX = (Math.random() - 0.5) * 0.5 * speedMultiplier;
                p.speedY = (Math.random() - 0.5) * 0.5 * speedMultiplier;
                
                if (isYoru) {
                    p.color = Math.random() > 0.5
                        ? `rgba(0, 243, 255, ${p.opacity})`
                        : `rgba(255, 91, 0, ${p.opacity})`;
                } else {
                    p.color = Math.random() > 0.7
                        ? `rgba(255, 70, 85, ${p.opacity})`
                        : `rgba(236, 232, 225, ${p.opacity * 0.5})`;
                }
            });
        }

        const particleCount = Math.min(80, Math.floor((canvas.width * canvas.height) / 15000));
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }

        function drawConnections() {
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 150) {
                        const opacity = (1 - dist / 150) * 0.15;
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        
                        const isYoru = document.body.classList.contains('yoru-mode');
                        ctx.strokeStyle = isYoru 
                            ? `rgba(0, 243, 255, ${opacity})` 
                            : `rgba(255, 70, 85, ${opacity})`;
                            
                        ctx.lineWidth = 0.5;
                        ctx.stroke();
                    }
                }
            }
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            particles.forEach(p => {
                p.update();
                p.draw();
            });

            drawConnections();
            animFrameId = requestAnimationFrame(animateParticles);
        }

        animateParticles();
    }


    const cursorGlow = document.getElementById('cursorGlow');
    const cursorDot = document.getElementById('cursorDot');

    if (cursorGlow && cursorDot) {
        const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

        if (!isTouchDevice) {
            let glowX = 0, glowY = 0;
            let targetX = 0, targetY = 0;

            document.addEventListener('mousemove', (e) => {
                targetX = e.clientX;
                targetY = e.clientY;
                cursorDot.style.left = e.clientX + 'px';
                cursorDot.style.top = e.clientY + 'px';
            });

            function updateGlow() {
                glowX += (targetX - glowX) * 0.08;
                glowY += (targetY - glowY) * 0.08;
                cursorGlow.style.left = glowX + 'px';
                cursorGlow.style.top = glowY + 'px';
                requestAnimationFrame(updateGlow);
            }
            updateGlow();
        } else {
            cursorGlow.style.display = 'none';
            cursorDot.style.display = 'none';
        }
    }


    const revealElements = document.querySelectorAll('.reveal');

    if (revealElements.length > 0) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        revealElements.forEach(el => revealObserver.observe(el));
    }


    const glowCards = document.querySelectorAll('.glow-card');

    glowCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--glow-x', x + 'px');
            card.style.setProperty('--glow-y', y + 'px');
        });
    });


    function initHeroTextAnimation() {
        const heroTitle = document.querySelector('.hero-title');
        if (!heroTitle || heroTitle.dataset.animated === 'true') return;

        heroTitle.dataset.animated = 'true';

        const originalHTML = heroTitle.innerHTML;

        function splitTextNode(node, startDelay) {
            let delay = startDelay;
            const fragment = document.createDocumentFragment();

            const text = node.textContent;
            for (let i = 0; i < text.length; i++) {
                if (text[i] === ' ') {
                    const space = document.createElement('span');
                    space.className = 'char-space';
                    fragment.appendChild(space);
                } else {
                    const charSpan = document.createElement('span');
                    charSpan.className = 'char';
                    charSpan.textContent = text[i];
                    charSpan.style.setProperty('--char-delay', delay + 's');
                    fragment.appendChild(charSpan);
                    delay += 0.04;
                }
            }
            return { fragment, delay };
        }

        function processNode(parent) {
            let delay = 0.3;
            const newNodes = [];

            parent.childNodes.forEach(child => {
                if (child.nodeType === Node.TEXT_NODE) {
                    const { fragment, delay: newDelay } = splitTextNode(child, delay);
                    delay = newDelay;
                    newNodes.push(fragment);
                } else if (child.nodeType === Node.ELEMENT_NODE) {
                    const clone = child.cloneNode(false);
                    let innerDelay = delay;

                    child.childNodes.forEach(innerChild => {
                        if (innerChild.nodeType === Node.TEXT_NODE) {
                            const { fragment, delay: newDelay } = splitTextNode(innerChild, innerDelay);
                            innerDelay = newDelay;
                            clone.appendChild(fragment);
                        } else {
                            clone.appendChild(innerChild.cloneNode(true));
                        }
                    });

                    delay = innerDelay;
                    newNodes.push(clone);
                }
            });

            parent.innerHTML = '';
            parent.classList.add('split-text');
            newNodes.forEach(n => parent.appendChild(n));
        }

        processNode(heroTitle);
    }


    function initTypewriter() {
        const tagline = document.querySelector('.hero-tagline');
        if (!tagline || tagline.dataset.typed === 'true') return;

        tagline.dataset.typed = 'true';
        tagline.classList.add('typewriter');
    }


    const counterElements = document.querySelectorAll('.counter-value');

    if (counterElements.length > 0) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.dataset.target, 10);
                    animateCounter(el, 0, target, 1200);
                    counterObserver.unobserve(el);
                }
            });
        }, { threshold: 0.5 });

        counterElements.forEach(el => counterObserver.observe(el));
    }

    function animateCounter(element, start, end, duration) {
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            const eased = 1 - (1 - progress) * (1 - progress);
            const current = Math.floor(start + (end - start) * eased);

            element.textContent = current + '%';

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }


    const progressBars = document.querySelectorAll('.progress-bar');

    if (progressBars.length > 0) {
        const observerOptions = { threshold: 0.1 };

        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const finalWidth = bar.getAttribute('data-width') || '0%';

                    bar.style.width = '0%';
                    bar.offsetHeight;

                    bar.style.width = finalWidth;

                    bar.classList.add('progress-bar-pulse');

                    observer.unobserve(bar);
                }
            });
        }, observerOptions);

        progressBars.forEach(bar => observer.observe(bar));
    }


    const heroBgText = document.querySelector('.hero-bg-text');

    if (heroBgText) {
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
            if (scrollY < window.innerHeight) {
                heroBgText.style.transform = `translateY(${scrollY * 0.15}px) translateX(${scrollY * 0.05}px)`;
                heroBgText.style.opacity = Math.max(0.02 - scrollY * 0.00003, 0);
            }
        });
    }


    const navbar = document.querySelector('.navbar');

    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 80) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }


    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.pageYOffset >= (sectionTop - 150)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current) && current !== '') {
                link.classList.add('active');
            }
        });
    });


    const contactForm = document.getElementById('contactForm');
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');

    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            showToast('MENGIRIM PESAN TRANSMISI...', 'info');

            const formData = new FormData(contactForm);

            try {
                const response = await fetch(contactForm.action, {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (response.ok) {
                    showToast(result.message || 'Pesan berhasil dikirim!', 'success');
                    contactForm.reset();
                } else {
                    showToast(result.message || 'Terjadi kesalahan saat mengirim.', 'error');
                }
            } catch (error) {
                showToast('Koneksi gagal. Coba lagi nanti.', 'error');
            }
        });
    }

    function showToast(message, type = 'success') {
        if (!toast || !toastMessage) return;

        toastMessage.textContent = message.toUpperCase();

        if (type === 'success') {
            toast.style.borderColor = '#ece8e1';
            toast.style.backgroundColor = '#1f2326';
        } else if (type === 'error') {
            toast.style.borderColor = '#ff4655';
            toast.style.backgroundColor = '#0f1923';
        } else {
            toast.style.borderColor = '#7e7e7e';
            toast.style.backgroundColor = '#1f2326';
        }

        toast.classList.remove('hidden');

        if (type !== 'info') {
            setTimeout(() => {
                toast.classList.add('hidden');
            }, 4000);
        }
    }


    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetEl = document.querySelector(targetId);
            if (targetEl) {
                targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ==========================================================================
    // AGENT YORU / DRIFT MODE FUNCTIONALITY & FLASH ANIMATION
    // ==========================================================================
    
    // Permanent Yoru Mode Activation
    document.body.classList.add('yoru-mode');
    setTimeout(() => {
        if (typeof updateParticleThemes === 'function') {
            updateParticleThemes();
        }
    }, 100);

});
