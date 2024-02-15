const articlesPaginationInitialization = (elSelector, dataUrl, locator = "", renderCallback) => {
    // Инициализация пагинации с использованием pagination.js
    $(elSelector).pagination({
        locator: locator,
        dataSource: dataUrl,
        pageSize: 10, // Количество статей на странице
        callback: renderCallback,
        totalNumberLocator: (response) => response.total 
    });

}