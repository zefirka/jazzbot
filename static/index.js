$(function run() {

	if ($.cookie('token')) {
		call('/login', {
			token: $.cookie('token')
		}).then(res => {
			$('.paranja').fadeOut(200);
			
			if (res.ok) {
				show(res, res.username)
			} else {
				$.removeCookie('token');
			}

		});
	} else {
		setTimeout(function () {
			$('.paranja').fadeOut(200);
		}, 800);
	}

	$('#login').on('click', event => {
		event.preventDefault();

		const start = Date.now();
		const required = 1000;

		const username = $('#username').val();
		const password = $('#password').val();

		const payload = {username, password}

		if (!username || !password) {
			return error({error: 'Specify username and password'}, 2000);
		}

		$('.b-spin').fadeIn(200);
		$('.b-form')
			.animate({'opacity': '0.3'}, 150);

		call('/login', payload)
		.then(data => {
			if (data.ok) {

				if ($('#remember').prop('checked')) {
					$.cookie('token', data.token, {
						expires: 14,
						path: '/'
					})
				} else {
					$.cookie('token', data.token);
				}

				show(data, username);
			} else {
				error(data, username);
			}
		});


	});
});


function call(url, payload, required = 1000) {
	const start = Date.now();

	return new Promise(resolve => {
		$.ajax({
			url: url,
			type: 'POST',
			data: JSON.stringify(payload)
		}).then(resolve);
	}).then(result => {
		const end = Date.now();

		if (end - start < required) {
			return new Promise(resolve => {
				setTimeout(() => resolve(result), required - end + start)
			});
		}

		return result;
	})
	.then(JSON.parse);
}

function compile(tpl, data, defaultName = ''){
	return $(`#tpl__${tpl}`).html().replace(/\{\w+\}/g, name => {
		return data[name.slice(1,-1)] || defaultName;
	});
}

function show(data, username) {
	$('.b-form__error').addClass('g-hidden');
	$('.b-controls').remove();
	
	$('.b-content').removeClass('g-hidden');
	$('.b-login-wrapper').removeClass('g-hidden');

	const html = data.users.map((user, i) => {
		user.itemId = i;
		return compile('row', user);
	});
	
	$('.b-table').html(html);
	
	$('.b-login-wrapper').html(compile('login', {
		username 
	}))

	$('.b-admin-controls-wrapper').html(compile('controls', {
		token: data.token
	}))

	$('.js-show-add').click(() => {
		$('.b-user-data').removeClass('g-hidden');
		$('.js-show-add').addClass('g-hidden');
	});

	$('.js-add').click(() => {
		const payload = {
			admin: username,
			username: $('[name="add_username"]').val(),
			userid: $('[name="add_userid"]').val(),
			token: $.cookie('token'),
		}

		$('.paranja').fadeIn(150);
		call('/add', payload, 800)
		.then(res => {
			if (res.ok) {
				$('.b-table').append(compile('row', Object.assign(payload, {itemId: data.users.length})))
				data.users.push(payload)
				$('.js-show-add').removeClass('g-hidden');
				$('.b-user-data').addClass('g-hidden');
				$([].pop.call($('.js-remove'))).click(onRemove);
			}
			$('.paranja').fadeOut(150);
		})
	});

	$('.js-cancel').click(() => {
		$('.js-show-add').removeClass('g-hidden');
	});
	
	$('.js-out').click(() => {
		$.removeCookie('token');
		document.location.href = document.location.href
	});

	$('.js-remove').click(onRemove);

	function onRemove() {
		const self = this;
		const payload = [].reduce.call($('input', $(this).parent()), (p, i) => {
			p[$(i).attr('name')] = $(i).val();
			return p
		}, {});
		
		$('.paranja').fadeIn(150);
		call('/remove', Object.assign(payload, {admin: username, token: $.cookie('token')}), 1000)
			.then(res => {
				$('.paranja').fadeOut(150);
				if (res.ok) {
					$(self).parent().remove();
				}
			})
	}

}

function error(data, timeout = 1000) {
	$('.b-spin').fadeOut(100);
	$('.b-form').animate({'opacity': '1'});

	$('.b-form__error')
		.removeClass('g-hidden')
		.show()
		.html(data.error);

	setTimeout(() => {
		$('.b-form__error').fadeOut(250, () => {
			$('.b-form__error').addClass('g-hidden').hide();
		});
	}, 1000)
}
