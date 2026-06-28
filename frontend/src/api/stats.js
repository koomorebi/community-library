import request from './request'

export const getStats = () => request.get('/stats')

// 借阅热度排行榜
export const getRanking = (params) => request.get('/stats/ranking', { params })
