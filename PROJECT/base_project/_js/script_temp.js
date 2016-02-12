var scoutboard = document.querySelector('#scout-board');
scoutboard.innerHTML = `
{{ #members }}
    {{ nome }}
{{ /members }}
`;

var dump = [
    {{ #members }}
        {
            "nome":"{{nome}}",
            "id":"{{id}}",
            "faceid":"{{faceId}}",
            "badges": {{ badges }}
        },
    {{ /members }}
];
