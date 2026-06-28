import request from './request'

export function getBorrows(params) {
  return request.get('/borrows', { params })
}

export function borrowBook(data) {
  return request.post('/borrows/borrow', data)
}

export function returnBook(data) {
  return request.post('/borrows/return', data)
}

export function renewBook(data) {
  return request.post('/borrows/renew', data)
}

export function undoBorrow(borrowId) {
  return request.post(`/borrows/undo/${borrowId}`)
}
