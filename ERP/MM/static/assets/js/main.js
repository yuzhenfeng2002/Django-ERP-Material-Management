const toGithub = () => {
    window.open('https://github.com/OUDUIDUI/NoticeKit');
}

const showLoading = (options) => {
    notice.showLoading(options);

    setTimeout(() => {
        notice.hideLoading()
    },3000)
}

const showMessage = (options) => {
    notice.showToast(options);
}