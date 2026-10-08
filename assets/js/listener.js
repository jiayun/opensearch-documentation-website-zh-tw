/* Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations. */
const yesButton = document.getElementById('yes');
const noButton = document.getElementById('no');
const numCharsLabel = document.getElementById('num-chars');
const sendButton = document.getElementById('send');
const commentTextArea = document.getElementById('comment');
const thankYouText = document.getElementById('thank-you');
const nav = document.getElementById('site-nav');
const versionPanel = document.getElementById('version-panel');

const actionHandlers = {
    submit_issue_click: () => typeof gtag === 'function' && gtag('event', 'submit_issue_click'),
    edit_page_click: () => typeof gtag === 'function' && gtag('event', 'edit_page_click'),
    forum_link_click: () => typeof gtag === 'function' && gtag('event', 'forum_link_click'),
    enable_send_button: () => { if (sendButton) sendButton.disabled = false; },
    send_feedback: () => sendFeedback(),
    switch_tab: (el) => switchTab({ target: el }, el.getAttribute('data-tab')),
    copy_code: (el) => copyCode(el),
    copy_as_curl: (el) => copyAsCurl(el),
    open_playground: (el) => openPlayground(el)
};

// Single click event listener for the entire document
document.addEventListener('click', function(event) {
    const { target } = event;

    // Handle old-style buttons first
    if (target.matches('.copy-button') && target.hasAttribute('data-text')) {
        window.navigator.clipboard.writeText(target.getAttribute('data-text'));
        return; // Exit early to avoid multiple handlers
    }

    // Handle new-style buttons and other clicks
    const action = target.dataset.action;
    if (action && actionHandlers[action]) {
        actionHandlers[action](target);
    }
});

// Event listeners
if (commentTextArea) {
    document.addEventListener('DOMContentLoaded', updateTextArea);
    commentTextArea.addEventListener('input', updateTextArea);
}

function debounce(fn, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
}

function handleNavScroll() {
    const currentVersionPanel = document.getElementById('version-panel');
    if (nav && currentVersionPanel) {
        if (nav.scrollTop > 0) {
            currentVersionPanel.classList.add('nav-shadow');
        } else {
            currentVersionPanel.classList.remove('nav-shadow');
        }
    }
}

if (nav) {
    nav.addEventListener('scroll', debounce(handleNavScroll, 100));
}

function updateTextArea() {
    if (!commentTextArea) return;
    const text = commentTextArea.value.trim();
    
    if ((!yesButton || !yesButton.checked) && (!noButton || !noButton.checked)) {
        if (sendButton) sendButton.disabled = text.length === 0;
    }

    // calculate the number of characters remaining
    const counter = 350 - commentTextArea.value.length;
    if (numCharsLabel) numCharsLabel.innerText = counter + " characters left";
}


function sendFeedback() {
    let helpful = 'none';
    if (yesButton && yesButton.checked) {
        helpful = 'yes';
    }
    else if (noButton && noButton.checked) {
        helpful = 'no';
    }
    
    let comment = commentTextArea ? commentTextArea.value.trim() : 'none';
    if(comment.length === 0) {
        comment = 'none';
    }

    if (helpful === 'none' && comment === 'none') return;

    // split the comment into 100-char parts because of GA limitation on custom dimensions
    const commentLines = ["", "", "", ""];
    for (let i = 0; i <= (comment.length - 1)/100; i++) {
        commentLines[i] = comment.substring(i * 100, Math.min((i + 1)*100, comment.length));
    }

    if (typeof gtag === 'function') {
        gtag('event', 'feedback_click', { 
            'helpful': helpful,
            'comment': commentLines[0],
            'comment_2': commentLines[1],
            'comment_3': commentLines[2],
            'comment_4': commentLines[3],
        });
    }

    // show the hidden feedback text
    if (thankYouText) thankYouText.classList.remove('hidden');

    // disable the feedback buttons
    if (yesButton) yesButton.disabled = true;
    if (noButton) noButton.disabled = true;

    // disable the text area
    if (commentTextArea) commentTextArea.disabled = true;

    // disable the send button
    if (sendButton) sendButton.disabled = true;
}

function switchTab(event, tabId) {
    const container = event.target.closest('.code-tabs');

    container.querySelectorAll('.tab.active, .tab-button.active').forEach(el => {
        el.classList.remove('active');
    });
    
    // Add active class to selected tab and button
    const selectedTab = container.querySelector(`#${tabId}`);
    selectedTab?.classList.add('active');
    event.target.classList.add('active');
}

function copyCode(button) {
    const codeBlock = button.closest('.code-container').querySelector('pre');
    const code = codeBlock.textContent.trim(); 
    window.navigator.clipboard.writeText(code);
}

function copyAsCurl(button) {
    const codeBlock = button.closest('.code-container').querySelector('pre');
    const code = codeBlock.textContent.trim(); 
    
    const lines = code.split('\n');
    const [method, path] = lines[0].trim().split(' ');
    const body = lines.slice(1).join('\n');
    
    const formattedPath = path.startsWith('/') ? path : '/' + path;
    const curlCommand = body 
        ? `curl -X ${method} "localhost:9200${formattedPath}" -H "Content-Type: application/json" -d '\n${body}\n'`
        : `curl -X ${method} "localhost:9200${formattedPath}"`;
        
    window.navigator.clipboard.writeText(curlCommand);
}

function openPlayground(button) {
    let query = button.getAttribute('data-query');

    // Replace source=otellogs with the playground index pattern
    query = query.replace(/source\s*=\s*otellogs/gi, 'source=logs-otel-v1*');

    // Remove trailing semicolons
    query = query.replace(/;\s*$/, '');

    const baseUrl = 'https://observability.playground.opensearch.org/w/AYexAG/app/explore/logs/#/';

    // The hash params are parsed as RISON by the app.
    // Encode query with encodeURIComponent so all special chars are safe inside RISON quotes.
    const encodedQuery = encodeURIComponent(query).replace(/'/g, "!'");

    const qParam = `(dataset:(id:'6766d4f0-3869-11f1-b2f2-5f6bda0002a3',timeFieldName:time,title:'logs-otel-v1*',type:INDEX_PATTERN),language:PPL,query:'${encodedQuery}')`;
    const gParam = `(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-6h,to:now))`;
    const aParam = `(legacy:(columns:!(body,severityText,resource.attributes.service.name),interval:auto,isDirty:!f,sort:!()),tab:(logs:(),patterns:(usingRegexPatterns:!f)),ui:(activeTabId:logs,showHistogram:!t))`;

    window.open(`${baseUrl}?_g=${gParam}&_q=${qParam}&_a=${aParam}`, '_blank');
}
