/**
 * IMAGE_DATA: 이미지의 제목과 태그(페이지 구분용)를 관리하는 데이터베이스
 * 형식: "파일명": { title: "제목", tags: ["태그"] }
 *   예) "img/delta-01.avif": { title: "Project One 1", tags: ["project1"] }
 * - 태그가 같은 사진은 ?page=태그 페이지에 모인다 (index.html의 Works 메뉴 href와 같아야 함)
 * - 태그가 없는 사진은 시리즈 페이지(?page=alpha 등, script.js의 SERIES_CONFIG)에서만 나온다
 */
const IMAGE_DATA = {
    // [alpha] Series — 가로(짝수)/세로(홀수) 섞임
    "img/alpha-01.avif": { title: "still life" },
    "img/alpha-02.avif": { title: "still life" },
    "img/alpha-03.avif": { title: "still life" },
    "img/alpha-04.avif": { title: "still life" },
    "img/alpha-05.avif": { title: "portrait" },
    "img/alpha-06.avif": { title: "portrait" },
    "img/alpha-07.avif": { title: "portrait" },
    "img/alpha-08.avif": { title: "portrait" },

    // [beta] Series
    "img/beta-01.avif": { title: "Beta 1" },
    "img/beta-02.avif": { title: "Beta 2" },
    "img/beta-03.avif": { title: "Beta 3" },
    "img/beta-04.avif": { title: "Beta 4" },
    "img/beta-05.avif": { title: "Beta 5" },
    "img/beta-06.avif": { title: "Beta 6" },
    "img/beta-07.avif": { title: "Beta 7" },
    "img/beta-08.avif": { title: "Beta 8" },

    // [gamma] Series — 01~06은 에디토리얼 페이지(?page=editorial1)에도 묶임
    "img/gamma-01.avif": { title: "Editorial Title", tags: ["editorial1"] },
    "img/gamma-02.avif": { title: "Editorial Title", tags: ["editorial1"] },
    "img/gamma-03.avif": { title: "Editorial Title", tags: ["editorial1"] },
    "img/gamma-04.avif": { title: "Editorial Title", tags: ["editorial1"] },
    "img/gamma-05.avif": { title: "Editorial Title", tags: ["editorial1"] },
    "img/gamma-06.avif": { title: "Editorial Title", tags: ["editorial1"] },
    "img/gamma-07.avif": { title: "Gamma 7" },
    "img/gamma-08.avif": { title: "Gamma 8" },

    // [delta] Series — 촬영(photoshoot) 페이지 3개로 나뉨 (?page=project1/2/3, 목록은 ?page=photoshoots)
    "img/delta-01.avif": { title: "Project One 1", tags: ["project1"] },
    "img/delta-02.avif": { title: "Project One 2", tags: ["project1"] },
    "img/delta-03.avif": { title: "Project One 3", tags: ["project1"] },
    "img/delta-04.avif": { title: "Project One 4", tags: ["project1"] },
    "img/delta-05.avif": { title: "Project One 5", tags: ["project1"] },
    "img/delta-06.avif": { title: "Project Two 1", tags: ["project2"] },
    "img/delta-07.avif": { title: "Project Two 2", tags: ["project2"] },
    "img/delta-08.avif": { title: "Project Two 3", tags: ["project2"] },
    "img/delta-09.avif": { title: "Project Two 4", tags: ["project2"] },
    "img/delta-10.avif": { title: "Project Three 1", tags: ["project3"] },
    "img/delta-11.avif": { title: "Project Three 2", tags: ["project3"] },
    "img/delta-12.avif": { title: "Project Three 3", tags: ["project3"] },

    // 기본 시리즈 이름 매핑 (특정 제목이 없을 때 사용)
    "series_alpha": "Series Alpha",
    "series_beta": "Series Beta",
    "series_gamma": "Series Gamma",
    "series_delta": "Series Delta"
};

/**
 * 특정 태그에 대응하는 페이지 링크 매핑 (사진 제목이 푸터에서 링크가 됨)
 * 외부 링크(영상 등)도 가능: "yt_example": "https://youtu.be/xxxxxxxx"
 */
const TAG_PAGES = {
    "project1": "?page=photoshoots",
    "project2": "?page=photoshoots",
    "project3": "?page=photoshoots",
    "editorial1": "?page=editorial1"
};

/* 사진 제목에 링크를 만들지 않을 페이지 */
const NO_TITLE_LINK_PAGES = [];

/**
 * 특정 이미지의 제목(Title)을 가져옵니다.
 * 링크가 가능한 태그가 있다면 <a> 태그를 포함하여 반환합니다.
 */
function getLabelFor(src) {
    let title = "Untitled";
    let tags = [];

    if (IMAGE_DATA[src]) {
        title = IMAGE_DATA[src].title || title;
        tags = IMAGE_DATA[src].tags || [];
    } else {
        // 파일명에서 시리즈 키 추출 (예: img/alpha-01.avif -> alpha)
        const match = src.match(/img\/([a-z0-9]+)-/);
        if (match) {
            const key = match[1];
            title = IMAGE_DATA[`series_${key}`] || title;
        }
    }

    // 링크 가능한 태그가 있는지 확인
    const linkTag = tags.find(tag => TAG_PAGES[tag]);

    // 현재 페이지 파라미터 확인
    const urlParams = new URLSearchParams(window.location.search);
    const pageParam = urlParams.get("page") || "alpha";

    if (linkTag && !NO_TITLE_LINK_PAGES.includes(pageParam)) {
        const url = TAG_PAGES[linkTag];
        const isExternal = url.startsWith("http");
        const target = isExternal ? 'target="_blank"' : "";
        return `<a href="${url}" ${target} class="footer-link">${title}</a>`;
    }

    return title;
}

/**
 * 특정 태그에 해당하는 모든 이미지 리스트를 가져옵니다.
 */
function getImagesByTag(tag) {
    return Object.keys(IMAGE_DATA).filter(path => {
        const data = IMAGE_DATA[path];
        return data && data.tags && data.tags.includes(tag);
    });
}
