tailwind.config = {
  theme: {
    extend: {
      fontFamily: {
        poppins: ["Poppins", "sans-serif"],
      },
    },
  },
};


// Show all blog After clicking Load more button

document.addEventListener("DOMContentLoaded", function () {
  const loadMoreBtn = document.getElementById("loadMoreBtn");
  const blogCards = document.querySelectorAll(".blog-card");

  loadMoreBtn.addEventListener("click", function () {
    blogCards.forEach((card) => card.classList.remove("hidden"));
    loadMoreBtn.style.display = "none";
  });
});

// Handle CSRF for Htmx

document.body.addEventListener("htmx:configRequest", (event) => {
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
  event.detail.headers["X-CSRFToken"] = csrfToken;
});

// Sidebar Toggle
const toggleBtn = document.getElementById("toggleSidebar");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");
const openIcon = document.getElementById("openIcon");
const closeIcon = document.getElementById("closeIcon");

toggleBtn.addEventListener("click", () => {
  const isOpen = sidebar.classList.contains("translate-x-0");

  if (isOpen) {
    sidebar.classList.remove("translate-x-0");
    sidebar.classList.add("-translate-x-full");
    overlay.classList.add("hidden");
    openIcon.classList.remove("hidden");
    closeIcon.classList.add("hidden");
  } else {
    sidebar.classList.remove("-translate-x-full");
    sidebar.classList.add("translate-x-0");
    overlay.classList.remove("hidden");
    openIcon.classList.add("hidden");
    closeIcon.classList.remove("hidden");
  }
});

overlay.addEventListener("click", () => {
  sidebar.classList.add("-translate-x-full");
  sidebar.classList.remove("translate-x-0");
  overlay.classList.add("hidden");
  openIcon.classList.remove("hidden");
  closeIcon.classList.add("hidden");
});

// All blog page category scroll

document.addEventListener("DOMContentLoaded", () => {
  const catScroll = document.getElementById("catScroll");
  const leftBtn = document.getElementById("leftBtn");
  const rightBtn = document.getElementById("rightBtn");

  leftBtn.addEventListener("click", () => {
    catScroll.scrollBy({ left: -200, behavior: "smooth" });
  });

  rightBtn.addEventListener("click", () => {
    catScroll.scrollBy({ left: 200, behavior: "smooth" });
  });
});

function toggleReplyBox(id) {
  const box = document.getElementById(id);
  if (box) {
    box.classList.toggle("hidden");
  }
}

// function postReply(commentId) {
//   const content = document.getElementById(`replyContent-${commentId}`).value;
//   const blogSlug = "{{ blog.slug }}";

//   if (content.trim()) {
//     fetch(`/category/blogs/${blogSlug}/comment/${commentId}/reply/`, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//         "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
//           .value,
//       },
//       body: JSON.stringify({ content: content }),
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         if (data.status === "success") {
//           const commentDiv = document.getElementById(`comment-${commentId}`);
//           const newReply = `
//               <div class="ml-10 mt-3 flex items-start gap-3">
//                 <div class="size-8 bg-blue-400 rounded-full flex items-center justify-center text-white font-semibold">${data.user[0]}</div>
//                 <div class="w-full">
//                   <p class="font-semibold">${data.user}</p>
//                   <p class="text-gray-800 mt-1 text-sm md:text-md">${data.content}</p>
//                 </div>
//               </div>
//           `;
//           commentDiv.insertAdjacentHTML("beforeend", newReply);
//           document.getElementById(`replyContent-${commentId}`).value = "";
//           toggleReplyBox(`reply-box-${commentId}`);
//         }
//       });
//   }
// }
