$(document).ready(function () {
    $('#myTable').DataTable({
        language: {
            "emptyTable": "暂无记录",
            "info": "",
            "infoEmpty": "",
            "loadingRecords": "加载中...",
            "processing": "处理中...",
            "lengthMenu": "显示 _MENU_ 行",
            "search": "搜索:",
            "zeroRecords": "没有记录",
            "paginate": {
                "first": "1",
                "last": "尾",
                "next": "->",
                "previous": "<-"
            },

        },
    });
});