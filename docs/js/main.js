const user = "1abhax";
const repo = "CTF";
const branch = "main";
const targetDir = "writeups";   // 你要讀的資料夾

async function loadDir(path="", container){

    const url =
    `https://api.github.com/repos/${user}/${repo}/contents/${path}?ref=${branch}`;

    const res = await fetch(url);
    const data = await res.json();

    data.forEach(item => {

        const div = document.createElement("div");

        if(item.type === "dir"){

            div.innerText = "📁 " + item.name;
            div.className = "folder";

            const sub = document.createElement("div");

            div.onclick = () => {
                if(sub.innerHTML === ""){
                    loadDir(item.path, sub);
                }
                sub.style.display =
                    sub.style.display === "none" ? "block" : "none";
            };

            container.appendChild(div);
            container.appendChild(sub);

        }else{

            div.innerText = "📄 " + item.name;
            div.className = "file";

            div.onclick = () => {
                document.getElementById("content").innerHTML =
                `<iframe src="${item.html_url}" width="100%" height="900"></iframe>`;
            };

            container.appendChild(div);
        }

    });
}

loadDir(targetDir, document.getElementById("sidebar"));

async function loadConfig(){

    const res = await fetch("data/config.json");
    const config = await res.json();

    return config;
}
async function start(){

    const config = await loadConfig();

    loadDir(config.content_dir,
            document.getElementById("sidebar"));
}

start();
