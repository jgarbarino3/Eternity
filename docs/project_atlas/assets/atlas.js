const state = {
  lane: "all",
  status: "all",
  query: "",
};

const nodes = Array.from(document.querySelectorAll(".atlas-node"));
const filterButtons = Array.from(document.querySelectorAll(".filter-button"));
const searchInput = document.querySelector("#atlas-search");
const emptyState = document.querySelector(".empty-state");
const navLinks = Array.from(document.querySelectorAll(".sidebar a"));
const sections = Array.from(document.querySelectorAll(".atlas-section"));

function normalize(value) {
  return value.trim().toLowerCase();
}

function nodeMatches(node) {
  const laneMatches = state.lane === "all" || node.dataset.lane === state.lane;
  const statusMatches = state.status === "all" || node.dataset.status === state.status;
  const queryMatches = !state.query || normalize(node.textContent).includes(state.query);
  return laneMatches && statusMatches && queryMatches;
}

function updateFilters() {
  let visibleCount = 0;

  nodes.forEach((node) => {
    const visible = nodeMatches(node);
    node.classList.toggle("filtered-out", !visible);
    if (visible) visibleCount += 1;
  });

  emptyState.hidden = visibleCount !== 0;
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const group = button.dataset.filterGroup;
    state[group] = button.dataset.filterValue;

    filterButtons
      .filter((candidate) => candidate.dataset.filterGroup === group)
      .forEach((candidate) => {
        candidate.classList.toggle("active", candidate === button);
      });

    updateFilters();
  });
});

searchInput.addEventListener("input", (event) => {
  state.query = normalize(event.target.value);
  updateFilters();
});

const observer = new IntersectionObserver(
  (entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

    if (!visible) return;

    navLinks.forEach((link) => {
      link.classList.toggle("active", link.getAttribute("href") === `#${visible.target.id}`);
    });
  },
  {
    rootMargin: "-20% 0px -62% 0px",
    threshold: [0.1, 0.3, 0.6],
  }
);

sections.forEach((section) => observer.observe(section));
updateFilters();
