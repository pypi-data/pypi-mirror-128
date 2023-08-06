$(document).ready(function () {
    $('.showBtn').each(function () {
        let block_id = $(this).data("block");
        if (block_id){
            let block = $('div[data-blockid='+block_id+']');
            if (block.attr('class').indexOf('d-none') > -1){
                this.innerHTML = '(Показать)';
            }
            else {
                this.innerHTML = '(Скрыть)';
            }
        }
    });
    $('.showBtn').click(function () {
        let block_id = $(this).data("block");
        let block = $('div[data-blockid='+block_id+']');

        if (block_id){
            if (this.innerHTML === '(Показать)') {
                this.innerHTML = '(Скрыть)';

                document.getElementById("data-" + block_id).innerHTML = '';
            }
            else {
                this.innerHTML = '(Показать)';

                let text = '';

                block.find('[data-param="true"]').each(function () {
                    let val = '';
                    let index = $(this).data('param-index');
                    if (index === 'text') if ($(this).is("select")) val = $('option:selected', this).text(); else val = $(this).text();
                    else if ($(this).is("select")) val = $('option:selected', this).val(); else val = $(this).val();
                    if ($(this).data('param-append-start')) text += $(this).data('param-append-start') + ' ';
                    text += val + ' ';
                    if ($(this).data('param-append-end')) text += $(this).data('param-append-end') + ' ';
                });
                document.getElementById("data-" + block_id).innerHTML = text;
            }
            block.toggleClass('d-none');
        }
    });
});