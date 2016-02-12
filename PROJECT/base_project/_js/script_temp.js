var scoutboard = document.querySelector('#scout-board');
scoutboard.innerHTML = `
{{ #members }}
    {{ nome }}
{{ /members }}
`;
