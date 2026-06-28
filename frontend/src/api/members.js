import request from './request'

export const getMembers = (params) => request.get('/members', { params })
export const getMember = (id) => request.get(`/members/${id}`)
export const createMember = (data) => request.post('/members', data)
export const updateMember = (id, data) => request.put(`/members/${id}`, data)
export const deleteMember = (id) => request.delete(`/members/${id}`)
export const getMemberDetail = (id) => request.get(`/members/${id}/detail`)
