import request from '@/utils/request'

export function action_task(data) {
  return request({
    url: '/api/domain/xxljob/action_task/',
    method: 'post',
    data
  })
}

export function save_code(data) {
  return request({
    url: '/api/domain/xxljob/save_code/',
    method: 'post',
    data
  })
}

export function chatinfo(data) {
  return request({
    url: '/api/domain/xxljob/chatinfo/',
    method: 'post',
    data
  })
}

export function domain_delay(data) {
  return request({
    url: '/api/domain/xxljob/domain_delay/',
    method: 'post',
    data
  })
}

export function get_group() {
  return request({
    url: '/boce/get_group/',
    method: 'get'
  })
}

export function create_group(data) {
  return request({
    url: '/boce/create_group/',
    method: 'post',
    data
  })
}

export function update_group(data) {
  return request({
    url: '/boce/update_group/',
    method: 'post',
    data
  })
}

export function delete_group(data) {
  return request({
    url: '/boce/delete_group/',
    method: 'post',
    data
  })
}

export function get_code_by_id(data) {
  return request({
    url: '/boce/get_code_by_id/',
    method: 'post',
    data
  })
}

export function get_code_history_by_id(data) {
  return request({
    url: '/boce/get_code_history_by_id/',
    method: 'post',
    data
  })
}

export function get_log_count() {
  return request({
    url: '/boce/get_log_count/',
    method: 'get'
  })
}