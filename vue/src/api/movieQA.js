import request from "@/utils/request";

const movieQARequest = {
    /**
     * 提交电影相关问题并获取回答
     * @param {string} question 用户提出的问题
     * @returns {Promise} 包含Cypher查询和自然语言回答的Promise
     */
    askMovieQuestion: (question) => {
        return request({
            url: '/movie/qa',
            method: 'post',
            timeout: 30000,
            headers: {
                isNeedToken: false,
                'Content-Type': 'application/json'
            },
            data: {
                question: question
            }
        }).then(response => {
            console.log(response);  // 打印API响应以调试
            if (response) {
            
                return response.answer;  // 直接返回answer内容
            }
            throw new Error('无效的响应格式')
        })
    },
    
    /**
     * 获取常见电影问题示例
     * @returns {Promise} 包含常见问题列表的Promise
     */
    getCommonQuestions: () => {
        return request({
            url: '/movie/qa/examples',
            method: 'get',
            headers: {
                isNeedToken: false
            }
        })
    },
    
    /**
     * 获取问答历史记录
     * @param {number} currentPage 当前页码
     * @param {number} pageSize 每页数量
     * @returns {Promise} 包含历史记录的Promise
     */
    getQaHistory: (currentPage, pageSize) => {
        return request({
            url: '/movie/qa/history',
            method: 'get',
            headers: {
                isNeedToken: true  // 历史记录需要登录
            },
            params: {
                currentPage,
                pageSize
            }
        })
    }
}

export default movieQARequest