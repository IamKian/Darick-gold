// ۱. مدیریت تغییر استایل هدر هنگام اسکرول
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 80) navbar.classList.add('scrolled');
    else navbar.classList.remove('scrolled');
});

// ۲. رندر کردن محصولات و اسلایدر
const products = [
    { name: "گردنبند رویال", price: "۴۵,۸۰۰,۰۰۰", img: "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600" },
    { name: "حلقه الماس", price: "۱۲۸,۰۰۰,۰۰۰", img: "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=600" },
    { name: "گوشواره زمرد", price: "۳۴,۲۰۰,۰۰۰", img: "https://images.unsplash.com/photo-1635767791022-94bc7175ad2b?w=600" },
    { name: "دستبند کارتیه", price: "۲۲,۰۰۰,۰۰۰", img: "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600" },
    { name: "ساعت رولکس", price: "۵۴۰,۰۰۰,۰۰۰", img: "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=600" }
];

const gridContainer = document.getElementById('product-list');
products.forEach((p) => {
    gridContainer.innerHTML += `
        <div class="swiper-slide">
            <div class="pro-card">
                <div class="pro-img-box">
                    <img src="${p.img}" alt="${p.name}">
                </div>
                <div class="pro-info">
                    <h3>${p.name}</h3>
                    <p class="pro-price">${p.price} تومان</p>
                </div>
            </div>
        </div>
    `;
});

const swiper = new Swiper(".productSwiper", {
    slidesPerView: 1,
    spaceBetween: 20,
    loop: true,
    autoplay: { delay: 3000 },
    pagination: { el: ".swiper-pagination", clickable: true },
    navigation: { nextEl: ".swiper-button-next", prevEl: ".swiper-button-prev" },
    breakpoints: {
        768: { slidesPerView: 2 },
        1024: { slidesPerView: 3 },
        1200: { slidesPerView: 4 }
    }
});

// ۳. افکت تایپ و پارالاکس
const typewriterElement = document.getElementById('typewriter');
const phrases = ["اصالت در تبلور طلا", "طراحی جواهرات سفارشی", "درخشش در لحظات خاص", "گالری طلا و جواهر داریک"];
let phraseIndex = 0, charIndex = 0, isDeleting = false, typeSpeed = 150;

function typeLoop() {
    const currentPhrase = phrases[phraseIndex];
    typewriterElement.textContent = isDeleting ? currentPhrase.substring(0, charIndex - 1) : currentPhrase.substring(0, charIndex + 1);
    charIndex = isDeleting ? charIndex - 1 : charIndex + 1;
    typeSpeed = isDeleting ? 80 : 150;

    if (!isDeleting && charIndex === currentPhrase.length) { isDeleting = true; typeSpeed = 2000; }
    else if (isDeleting && charIndex === 0) { isDeleting = false; phraseIndex = (phraseIndex + 1) % phrases.length; typeSpeed = 500; }
    setTimeout(typeLoop, typeSpeed);
}

// ۴. مدیریت هوشمند ورود و مودال
const modal = document.getElementById('authModal');
const cartBtn = document.querySelector('.cart-btn');
const closeBtn = document.getElementById('closeModal');
const userBtn = document.getElementById('openAuth'); // آیدی جدید برای آیکون اکانت
closeBtn.onclick = function() {
    modal.style.display = "none"; // مخفی کردن مودال
    document.body.style.overflow = "auto"; // فعال کردن مجدد اسکرول صفحه
}
// تابع چک کردن وضعیت ورود
const userMenu = document.getElementById('userMenu');

function checkLoginAndOpen(e) {
    e.stopPropagation(); // جلوگیری از بسته شدن آنی منو
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    
    if (isLoggedIn === 'true') {
        // اگر وارد شده، منوی دراپ‌داون را باز و بسته کن
        userMenu.classList.toggle('show');
    } else {
        // اگر وارد نشده، مودال ورود را باز کن
        openAuthModal();
    }
}

// بستن منو با کلیک روی هر جای دیگر صفحه
window.addEventListener('click', () => {
    if (userMenu.classList.contains('show')) {
        userMenu.classList.remove('show');
    }
});

// تابع خروج
function logout() {
    localStorage.removeItem('isLoggedIn');
    alert("شما با موفقیت خارج شدید.");
    location.reload(); 
}

// اتصال به دکمه
userBtn.onclick = checkLoginAndOpen;

function openAuthModal() {
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
    const content = document.querySelector('.modal-content');
    content.style.opacity = "0";
    content.style.transform = "translateY(-20px)";
    setTimeout(() => {
        content.style.transition = "all 0.5s ease";
        content.style.opacity = "1";
        content.style.transform = "translateY(0)";
    }, 10);
}

// رویداد کلیک دکمه‌ها
// تابع اختصاصی برای کلیک روی سبد خرید
cartBtn.onclick = function() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    
    if (isLoggedIn === 'true') {
        // در اینجا به جای باز کردن فرم ورود، پنل سبد خرید را نشان می‌دهیم
        // فعلاً برای تست یک Alert نشان می‌دهیم، بعداً می‌توانید لیست خرید را اینجا رندر کنید
        alert("در حال باز کردن لیست خرید شما..."); 
        
        // اگر در آینده بخش سبد خرید (Cart Drawer) ساختید، آن را اینجا باز کنید:
        // openCartDrawer(); 
    } else {
        // اگر وارد نشده بود، فرم ورود را باز کن
        openAuthModal();
    }
};

// تابع اختصاصی برای کلیک روی آیکون اکانت (همان منوی دراپ‌داونی که ساختیم)
userBtn.onclick = function(e) {
    e.stopPropagation();
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    
    if (isLoggedIn === 'true') {
        userMenu.classList.toggle('show');
    } else {
        openAuthModal();
    }
};

window.onclick = (event) => {
    if (event.target == modal) {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }
};

// ۵. مدیریت فرم‌ها و ذخیره وضعیت ورود
// اصلاح تابع سوییچ بین فرم‌ها
function switchForm(type) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const tabs = document.querySelectorAll('.tab-btn');

    if (type === 'login') {
        loginForm.classList.add('active');
        registerForm.classList.remove('active');
        tabs[0].classList.add('active');
        tabs[1].classList.remove('active');
    } else {
        registerForm.classList.add('active');
        loginForm.classList.remove('active'); // این خط اصلاح شد
        tabs[1].classList.add('active');
        tabs[0].classList.remove('active');
    }
}

// تابع خروج (Logout) برای تست
function logout() {
    localStorage.removeItem('isLoggedIn');
    alert("از حساب خارج شدید.");
    location.reload(); // صفحه رفرش شود تا تغییرات اعمال شود
}

// شبیه‌سازی ورود موفق
const handleAuth = (e, loaderId, message) => {
    e.preventDefault();
    const form = e.target;
    const btn = form.querySelector('.btn-main');
    const loader = document.getElementById(loaderId);

    btn.style.display = 'none';
    loader.style.display = 'block';

    setTimeout(() => {
        localStorage.setItem('isLoggedIn', 'true'); // ذخیره وضعیت در مرورگر
        alert(message);
        modal.style.display = "none";
        document.body.style.overflow = "auto";
        loader.style.display = 'none';
        btn.style.display = 'block';
    }, 3000);
};

document.getElementById('loginForm').onsubmit = (e) => handleAuth(e, 'loginLoader', 'خوش آمدید!');
document.getElementById('registerForm').onsubmit = (e) => handleAuth(e, 'registerLoader', 'حساب شما ساخته شد!');

// ۶. سایر انیمیشن‌ها
window.addEventListener('load', () => {
    setTimeout(typeLoop, 1000);
    const mainBtn = document.querySelector('.btn-main');
    setTimeout(() => {
        mainBtn.style.transform = 'scale(1.05)';
        setTimeout(() => mainBtn.style.transform = 'scale(1)', 200);
    }, 1500);
});

document.querySelector('.btn-main').addEventListener('click', () => {
    document.querySelector('.shop-container').scrollIntoView({ behavior: 'smooth' });
});
// داخل تایم‌اوتِ مربوط به لاگین موفق:
document.querySelector('.cart-btn').style.color = '#d4af37';
window.onclick = function(event) {
    // اگر کاربر روی فضای سیاه پشت مودال کلیک کرد
    if (event.target == modal) {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }
}

