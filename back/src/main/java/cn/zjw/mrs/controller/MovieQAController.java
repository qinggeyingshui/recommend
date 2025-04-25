package cn.zjw.mrs.controller;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;
import java.util.*;

@RestController
@RequestMapping("/movie")
//@CrossOrigin(origins = "*", allowedHeaders = "*")
public class MovieQAController {

    private final String PYTHON_API_URL = "http://127.0.0.1:5000/movie/qa";
    private final RestTemplate restTemplate;

    public MovieQAController(@Qualifier("corsRestTemplate") RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @PostMapping("/qa")
    public ResponseEntity<Map<String, String>> handleQuestion(@RequestBody Map<String, String> request) {
        try {
            // 设置请求头
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            // 构建请求体
            Map<String, String> body = new HashMap<>();
            body.put("question", request.get("question"));

            HttpEntity<Map<String, String>> entity = new HttpEntity<>(body, headers);

            // 调用Python API
            ResponseEntity<Map> response = restTemplate.postForEntity(
                    PYTHON_API_URL,
                    entity,
                    Map.class
            );

            // 获取响应数据并提取answer字段
            Map<String, Object> responseBody = response.getBody();
            Map<String, String> result = new HashMap<>();
            result.put("answer", responseBody.get("answer").toString());
            return ResponseEntity.ok(result);

        } catch (Exception e) {
            Map<String, String> errorResult = new HashMap<>();
            errorResult.put("error", "调用问答服务失败: " + (e.getMessage() != null ? e.getMessage() : "未知错误"));
            return ResponseEntity.status(500).body(errorResult);
        }
    }

    @GetMapping("/qa/examples")
    public List<String> getCommonQuestions() {
        return Arrays.asList(
                "推荐几部高评分喜剧片",
                "汤姆·汉克斯演过哪些电影？",
                "克里斯托弗·诺兰导演的电影有哪些？",
                "2010年后评分高于8分的科幻片"
        );
    }
}