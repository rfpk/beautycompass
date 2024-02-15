// Сортировка по
const sortedBy = document.getElementById('sortedBy');
if (sortedBy) {
    sortedBy.addEventListener('change', (e) => {
        addQueryParam(`sort_by=${sortedBy.value}`, 'sorted');
    })
}

// Add Query Parameters
function addQueryParam(href, type) {
    let splitHref = href.split('=');
    let url = new URL(location.href);
    let queryString = url.search;
    let searchParams = new URLSearchParams(queryString);
    
    if (splitHref[0] && splitHref[1]) {
        if (type === 'pagination' || type === 'sorted') {
            searchParams.set(splitHref[0], splitHref[1])
        } else if (type === 'tags') {
            let tags = searchParams.getAll('tag');
            let isInclude = tags.includes(splitHref[1])
            if (isInclude) {
                searchParams.delete(splitHref[0], splitHref[1]);
            } else {
                searchParams.append(splitHref[0], splitHref[1]);
            }
            // Delete Page Param
            searchParams.delete('page', searchParams.get('page'));
        } else {
            searchParams.append(splitHref[0], splitHref[1])
            // Delete Page Param
            searchParams.delete('page', searchParams.get('page'));
        }
    }
    location.search = searchParams;
}