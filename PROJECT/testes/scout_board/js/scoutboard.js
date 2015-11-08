var scoutboard = document.querySelector('#scout-board');

scoutboard.innerHTML = `
<table class="tg table table-striped table-bordered" style="margin-bottom: 10px; fixed; width: 100%">
    <colgroup>
        <col style="width: 50px">
        <col style="width: 150px">
    </colgroup>
    <tbody>
        <tr>
            <!-- CREST ICON -->
            <th class="crest">
                <img alt="crest" class="crestpic" title="!{crest[0]}" src="{PATH + crest[1]}.png">
            </th>
            <!-- NAME -->
            <th align="left" class="name" colspan="3"> !{mito.name} </th>
            <!-- Espacinho -->
            <!-- TIER -->
            <th align="left" class="tiername">
                <span class="tierlevel"> !{mito.tier[2]} </span>{{ table.tier }}:
                <strong> !{mito.tier[0]}</strong>
            </th>
            <th align="right" class="tiericon">
                <div>
                    <img alt="tier" class="tier" title="!{mito.tier[1][0]}" src="!{PATH + mito.tier[1][1]}.png">
            </th>
        </tr>
        <tr>
            <!-- PROFILE PIC -->
            <td align="center" class="profilepic" colspan="2" rowspan="5">
                <a target="_blank" href="https://www.facebook.com/!{mito.faceId}">
                    <img alt="profile" class="profile" src="http://graph.facebook.com/!{mito.faceId}/picture?width=151&height=151">
                </a>
            </td>
            <tr>
                <td HEIGHT="1px" colspan="2"></td>
            </tr>
            <td class="tg-e3zv">
                {{table.badges}}
            </td>
            <td class="tg-031e"></td>
            <td class="since" align="right" colspan="3"> {{ table.since }}
                <strong class="mythano"> !{mito.ano} </strong>
            </td>
        </tr>
        <tr>
            <!-- BADGES -->
            <td class="badges" id="!{mito.tagId}" colspan="4">
                Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </td>
        </tr>
        <tr>

                    <td colspan="4" align="right" class="badges2"> <i>{{ table.collection }}</i> <b id="!{mito.tagId1}"></b> </td>
        </tr>
    </tbody>
</table>
`;
