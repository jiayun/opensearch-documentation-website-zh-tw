/* Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations. */
const contributeButton = document.getElementById('contribute');

if (contributeButton && contributeButton.addEventListener) {
    contributeButton.addEventListener('click', function(event) {
        window.open('https://github.com/jiayun/opensearch-documentation-website-zh-tw/tree/3.9-zh-tw', '_blank');
    });
}
