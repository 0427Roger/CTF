const walker = document.createTreeWalker(
    document,
    NodeFilter.SHOW_COMMENT,
    null,
    false
);

const allComments = [];
while (walker.nextNode()) {
    allComments.push(walker.currentNode.nodeValue);
}
console.log(allComments);