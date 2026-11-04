# Pool run 3: base `claude-haiku-5-5` (effort default, adaptive thinking)

300 questions processed; 0 hit the 16,000-token cap, gave no FINAL ANSWER or failed claim extraction, and are excluded; base model wrong on **44** of 300 answered. API cost $2.3406. Contentions are the claims in the visible answer (DEVIATIONS.md, D1–D3).

Test set rule: D6: all wrong items (at most 40, at random) + an equal number of right items at random (seed 2026). Test set: 40 wrong + 40 right. Calibration pool: 220 items.

| id | category | truth | model | correct | set | contentions | related pairs | contradictions |
|---|---|---|---|---|---|---|---|---|
| h001 | simpleqa | yes | yes | yes | calib | 9 | 17 | 2 |
| h002 | claim | yes | yes | yes | calib | 10 | 32 | 7 |
| h003 | simpleqa | no | no | yes | calib | 8 | 12 | 6 |
| h004 | simpleqa | yes | no | **no** | test | 8 | 19 | 4 |
| h005 | simpleqa | yes | yes | yes | calib | 9 | 20 | 4 |
| h006 | claim | no | no | yes | calib | 8 | 14 | 3 |
| h007 | science-chemistry | no | no | yes | calib | 8 | 28 | 0 |
| h008 | claim | yes | yes | yes | test | 9 | 15 | 3 |
| h009 | claim | yes | yes | yes | calib | 9 | 31 | 7 |
| h010 | claim | no | no | yes | calib | 10 | 41 | 15 |
| h011 | claim | no | no | yes | calib | 9 | 16 | 0 |
| h012 | simpleqa | yes | yes | yes | calib | 8 | 12 | 2 |
| h013 | science-chemistry | yes | no | **no** | test | 9 | 25 | 0 |
| h014 | science-chemistry | yes | yes | yes | calib | 8 | 22 | 2 |
| h015 | science-chemistry | yes | yes | yes | calib | 9 | 26 | 0 |
| h016 | simpleqa | no | no | yes | calib | 8 | 19 | 3 |
| h017 | science-chemistry | yes | yes | yes | calib | 10 | 32 | 1 |
| h018 | simpleqa | yes | no | **no** | test | 9 | 22 | 6 |
| h019 | science-chemistry | yes | yes | yes | calib | 9 | 21 | 8 |
| h020 | science-chemistry | no | no | yes | calib | 9 | 18 | 1 |
| h021 | claim | yes | yes | yes | calib | 9 | 19 | 0 |
| h022 | claim | yes | yes | yes | calib | 8 | 18 | 0 |
| h023 | simpleqa | no | no | yes | calib | 7 | 15 | 0 |
| h024 | science-physics | yes | yes | yes | calib | 9 | 17 | 2 |
| h025 | simpleqa | yes | yes | yes | calib | 8 | 18 | 5 |
| h026 | simpleqa | yes | yes | yes | calib | 8 | 13 | 5 |
| h027 | simpleqa | yes | no | **no** | test | 9 | 24 | 6 |
| h028 | science-physics | no | no | yes | test | 9 | 25 | 3 |
| h029 | claim | no | no | yes | calib | 8 | 12 | 6 |
| h030 | science-physics | no | no | yes | calib | 10 | 30 | 2 |
| h031 | science-physics | no | no | yes | calib | 8 | 13 | 1 |
| h032 | science-physics | no | no | yes | calib | 8 | 26 | 0 |
| h033 | claim | yes | yes | yes | calib | 9 | 19 | 8 |
| h034 | science-physics | yes | yes | yes | test | 10 | 34 | 0 |
| h035 | science-physics | no | no | yes | calib | 7 | 17 | 4 |
| h036 | simpleqa | no | no | yes | calib | 9 | 12 | 3 |
| h037 | science-physics | yes | yes | yes | calib | 9 | 25 | 3 |
| h038 | science-chemistry | no | no | yes | calib | 9 | 36 | 0 |
| h039 | science-physics | yes | no | **no** | test | 10 | 36 | 12 |
| h040 | simpleqa | no | no | yes | calib | 9 | 21 | 0 |
| h041 | claim | no | no | yes | calib | 8 | 16 | 0 |
| h042 | science-chemistry | no | no | yes | test | 10 | 24 | 0 |
| h043 | science-physics | no | no | yes | calib | 9 | 23 | 3 |
| h044 | simpleqa | no | no | yes | calib | 8 | 14 | 0 |
| h045 | claim | no | no | yes | calib | 8 | 12 | 3 |
| h046 | simpleqa | yes | no | **no** | test | 8 | 15 | 2 |
| h047 | simpleqa | yes | yes | yes | calib | 8 | 12 | 0 |
| h048 | science-chemistry | yes | yes | yes | calib | 9 | 25 | 10 |
| h049 | science-physics | no | no | yes | calib | 7 | 20 | 6 |
| h050 | science-chemistry | yes | yes | yes | calib | 9 | 14 | 0 |
| h051 | science-physics | yes | yes | yes | calib | 8 | 16 | 2 |
| h052 | science-chemistry | no | no | yes | calib | 9 | 14 | 0 |
| h053 | simpleqa | yes | yes | yes | calib | 7 | 12 | 6 |
| h054 | simpleqa | no | no | yes | calib | 8 | 17 | 0 |
| h055 | simpleqa | yes | yes | yes | calib | 8 | 18 | 10 |
| h056 | simpleqa | yes | yes | yes | calib | 10 | 31 | 12 |
| h057 | science-chemistry | yes | no | **no** | test | 9 | 27 | 0 |
| h058 | science-physics | yes | no | **no** | test | 9 | 35 | 15 |
| h059 | science-physics | yes | yes | yes | calib | 9 | 20 | 2 |
| h060 | claim | yes | yes | yes | calib | 9 | 26 | 0 |
| h061 | simpleqa | yes | yes | yes | calib | 9 | 17 | 5 |
| h062 | science-physics | no | no | yes | calib | 9 | 27 | 0 |
| h063 | simpleqa | yes | yes | yes | calib | 8 | 15 | 5 |
| h064 | science-physics | yes | yes | yes | calib | 10 | 22 | 0 |
| h065 | science-physics | yes | no | **no** | test | 9 | 22 | 9 |
| h066 | science-physics | yes | yes | yes | calib | 9 | 19 | 2 |
| h067 | simpleqa | no | no | yes | calib | 8 | 28 | 0 |
| h068 | claim | yes | yes | yes | calib | 8 | 17 | 3 |
| h069 | claim | yes | yes | yes | calib | 8 | 15 | 0 |
| h070 | science-physics | yes | yes | yes | calib | 8 | 22 | 3 |
| h071 | claim | no | no | yes | calib | 9 | 29 | 7 |
| h072 | claim | no | no | yes | calib | 9 | 20 | 5 |
| h073 | claim | no | no | yes | calib | 8 | 22 | 10 |
| h074 | simpleqa | no | no | yes | calib | 8 | 14 | 0 |
| h075 | simpleqa | yes | no | **no** | test | 10 | 16 | 1 |
| h076 | claim | yes | yes | yes | calib | 9 | 14 | 0 |
| h077 | science-physics | yes | yes | yes | test | 8 | 22 | 1 |
| h078 | science-chemistry | yes | yes | yes | calib | 8 | 28 | 0 |
| h079 | science-physics | no | no | yes | calib | 8 | 25 | 0 |
| h080 | claim | yes | yes | yes | calib | 10 | 33 | 10 |
| h081 | science-physics | no | no | yes | calib | 8 | 20 | 5 |
| h082 | simpleqa | yes | yes | yes | calib | 9 | 17 | 6 |
| h083 | simpleqa | no | no | yes | calib | 8 | 23 | 6 |
| h084 | simpleqa | no | no | yes | calib | 8 | 13 | 0 |
| h085 | simpleqa | no | no | yes | calib | 8 | 18 | 3 |
| h086 | simpleqa | no | no | yes | calib | 9 | 16 | 6 |
| h087 | claim | yes | yes | yes | calib | 8 | 24 | 0 |
| h088 | science-chemistry | yes | no | **no** | test | 8 | 14 | 4 |
| h089 | simpleqa | yes | yes | yes | calib | 8 | 20 | 7 |
| h090 | claim | yes | yes | yes | calib | 9 | 23 | 7 |
| h091 | claim | no | no | yes | test | 10 | 18 | 6 |
| h092 | science-physics | yes | yes | yes | calib | 9 | 22 | 4 |
| h093 | science-chemistry | yes | yes | yes | calib | 8 | 16 | 5 |
| h094 | simpleqa | yes | yes | yes | calib | 9 | 16 | 6 |
| h095 | claim | yes | yes | yes | calib | 9 | 23 | 0 |
| h096 | simpleqa | yes | yes | yes | calib | 9 | 10 | 3 |
| h097 | claim | no | no | yes | calib | 9 | 25 | 3 |
| h098 | claim | no | no | yes | calib | 10 | 21 | 2 |
| h099 | simpleqa | yes | yes | yes | calib | 8 | 9 | 4 |
| h100 | simpleqa | no | no | yes | calib | 9 | 22 | 4 |
| h101 | simpleqa | no | yes | **no** | test | 8 | 19 | 10 |
| h102 | simpleqa | yes | no | **no** | test | 9 | 19 | 5 |
| h103 | science-physics | yes | no | **no** | test | 8 | 20 | 4 |
| h104 | claim | yes | yes | yes | calib | 9 | 18 | 0 |
| h105 | science-chemistry | yes | no | **no** | test | 8 | 22 | 2 |
| h106 | simpleqa | no | no | yes | calib | 8 | 16 | 0 |
| h107 | science-chemistry | no | no | yes | calib | 8 | 18 | 0 |
| h108 | science-chemistry | no | no | yes | calib | 8 | 19 | 0 |
| h109 | simpleqa | no | no | yes | test | 8 | 23 | 6 |
| h110 | simpleqa | yes | yes | yes | test | 9 | 19 | 4 |
| h111 | science-physics | yes | no | **no** | test | 8 | 23 | 8 |
| h112 | simpleqa | no | yes | **no** | test | 9 | 27 | 11 |
| h113 | science-physics | yes | yes | yes | calib | 8 | 21 | 5 |
| h114 | claim | no | no | yes | calib | 10 | 28 | 6 |
| h115 | simpleqa | yes | no | **no** | test | 7 | 11 | 3 |
| h116 | simpleqa | no | no | yes | calib | 8 | 20 | 0 |
| h117 | claim | no | no | yes | calib | 9 | 20 | 0 |
| h118 | science-chemistry | no | no | yes | calib | 9 | 29 | 1 |
| h119 | science-physics | yes | yes | yes | calib | 9 | 31 | 12 |
| h120 | science-physics | no | no | yes | test | 5 | 10 | 2 |
| h121 | simpleqa | yes | yes | yes | test | 9 | 23 | 5 |
| h122 | science-chemistry | yes | yes | yes | calib | 9 | 21 | 0 |
| h123 | simpleqa | yes | yes | yes | calib | 8 | 13 | 1 |
| h124 | claim | yes | yes | yes | calib | 10 | 31 | 8 |
| h125 | science-physics | no | no | yes | calib | 9 | 26 | 0 |
| h126 | science-physics | yes | yes | yes | test | 10 | 21 | 3 |
| h127 | simpleqa | yes | no | **no** | test | 9 | 14 | 4 |
| h128 | simpleqa | yes | yes | yes | test | 8 | 14 | 4 |
| h129 | science-physics | no | no | yes | calib | 9 | 16 | 0 |
| h130 | science-physics | yes | yes | yes | calib | 9 | 29 | 3 |
| h131 | claim | no | no | yes | calib | 10 | 22 | 9 |
| h132 | claim | no | no | yes | calib | 9 | 17 | 2 |
| h133 | simpleqa | no | no | yes | calib | 7 | 11 | 5 |
| h134 | simpleqa | no | no | yes | calib | 8 | 16 | 3 |
| h135 | science-chemistry | yes | no | **no** | test | 9 | 29 | 11 |
| h136 | science-chemistry | yes | yes | yes | calib | 10 | 18 | 3 |
| h137 | simpleqa | yes | no | **no** | test | 9 | 23 | 10 |
| h138 | science-chemistry | yes | no | **no** | test | 10 | 21 | 0 |
| h139 | simpleqa | no | no | yes | calib | 8 | 16 | 0 |
| h140 | simpleqa | yes | no | **no** | test | 9 | 11 | 1 |
| h141 | simpleqa | no | no | yes | test | 8 | 22 | 6 |
| h142 | simpleqa | yes | yes | yes | test | 8 | 17 | 8 |
| h143 | simpleqa | no | no | yes | calib | 7 | 15 | 0 |
| h144 | simpleqa | no | no | yes | calib | 7 | 15 | 5 |
| h145 | simpleqa | yes | yes | yes | calib | 7 | 11 | 0 |
| h146 | science-chemistry | yes | yes | yes | test | 9 | 22 | 0 |
| h147 | science-physics | no | no | yes | calib | 9 | 25 | 2 |
| h148 | claim | no | no | yes | calib | 9 | 15 | 0 |
| h149 | simpleqa | yes | yes | yes | test | 10 | 14 | 6 |
| h150 | simpleqa | yes | yes | yes | calib | 10 | 11 | 4 |
| h151 | simpleqa | no | no | yes | test | 8 | 18 | 0 |
| h152 | simpleqa | yes | no | **no** | calib | 9 | 19 | 7 |
| h153 | science-chemistry | no | no | yes | calib | 8 | 20 | 3 |
| h154 | science-chemistry | no | no | yes | test | 8 | 14 | 0 |
| h155 | claim | yes | yes | yes | calib | 8 | 9 | 0 |
| h156 | science-chemistry | no | no | yes | test | 9 | 21 | 5 |
| h157 | science-physics | no | no | yes | calib | 8 | 20 | 0 |
| h158 | claim | yes | yes | yes | calib | 9 | 22 | 9 |
| h159 | science-chemistry | yes | no | **no** | calib | 9 | 28 | 5 |
| h160 | science-chemistry | yes | yes | yes | test | 9 | 17 | 0 |
| h161 | science-physics | no | no | yes | calib | 9 | 13 | 2 |
| h162 | simpleqa | no | no | yes | calib | 9 | 18 | 1 |
| h163 | simpleqa | no | no | yes | calib | 9 | 23 | 8 |
| h164 | science-chemistry | yes | yes | yes | calib | 9 | 17 | 3 |
| h165 | science-chemistry | no | no | yes | calib | 8 | 17 | 0 |
| h166 | simpleqa | yes | yes | yes | calib | 8 | 15 | 6 |
| h167 | science-physics | no | no | yes | test | 9 | 15 | 3 |
| h168 | science-physics | no | no | yes | calib | 8 | 20 | 0 |
| h169 | science-physics | no | no | yes | calib | 8 | 20 | 8 |
| h170 | simpleqa | yes | yes | yes | test | 9 | 23 | 11 |
| h171 | simpleqa | yes | yes | yes | calib | 8 | 19 | 4 |
| h172 | science-physics | no | no | yes | calib | 8 | 17 | 0 |
| h173 | simpleqa | no | no | yes | test | 9 | 24 | 12 |
| h174 | simpleqa | no | no | yes | calib | 9 | 18 | 4 |
| h175 | science-chemistry | no | no | yes | test | 8 | 23 | 5 |
| h176 | science-chemistry | no | no | yes | calib | 9 | 33 | 7 |
| h177 | simpleqa | no | no | yes | calib | 8 | 15 | 6 |
| h178 | simpleqa | no | no | yes | calib | 9 | 28 | 7 |
| h179 | claim | no | no | yes | test | 8 | 22 | 6 |
| h180 | science-physics | no | no | yes | calib | 10 | 30 | 0 |
| h181 | science-physics | no | no | yes | calib | 8 | 18 | 0 |
| h182 | claim | yes | yes | yes | calib | 8 | 14 | 0 |
| h183 | claim | no | no | yes | calib | 9 | 11 | 6 |
| h184 | science-physics | no | no | yes | calib | 8 | 17 | 1 |
| h185 | simpleqa | no | no | yes | calib | 8 | 11 | 2 |
| h186 | simpleqa | no | no | yes | calib | 8 | 12 | 3 |
| h187 | simpleqa | yes | yes | yes | calib | 10 | 16 | 3 |
| h188 | claim | yes | yes | yes | calib | 9 | 16 | 1 |
| h189 | simpleqa | no | no | yes | calib | 9 | 27 | 0 |
| h190 | simpleqa | no | yes | **no** | calib | 7 | 16 | 7 |
| h191 | simpleqa | no | yes | **no** | test | 10 | 21 | 6 |
| h192 | science-physics | yes | yes | yes | calib | 9 | 31 | 0 |
| h193 | simpleqa | yes | yes | yes | test | 8 | 10 | 4 |
| h194 | simpleqa | yes | no | **no** | test | 9 | 17 | 0 |
| h195 | claim | yes | yes | yes | calib | 8 | 20 | 4 |
| h196 | claim | no | no | yes | calib | 8 | 25 | 0 |
| h197 | simpleqa | yes | no | **no** | test | 8 | 23 | 6 |
| h198 | simpleqa | yes | yes | yes | calib | 8 | 17 | 0 |
| h199 | simpleqa | no | no | yes | calib | 8 | 21 | 6 |
| h200 | science-chemistry | no | no | yes | calib | 9 | 26 | 0 |
| h201 | simpleqa | yes | yes | yes | calib | 8 | 19 | 9 |
| h202 | simpleqa | no | no | yes | calib | 8 | 14 | 1 |
| h203 | science-physics | yes | yes | yes | calib | 8 | 24 | 6 |
| h204 | simpleqa | yes | no | **no** | test | 9 | 21 | 1 |
| h205 | science-chemistry | no | no | yes | calib | 8 | 20 | 0 |
| h206 | simpleqa | no | no | yes | calib | 9 | 9 | 0 |
| h207 | science-chemistry | yes | yes | yes | calib | 8 | 21 | 6 |
| h208 | claim | no | no | yes | calib | 7 | 9 | 0 |
| h209 | claim | yes | yes | yes | calib | 8 | 20 | 6 |
| h210 | science-physics | yes | yes | yes | calib | 10 | 24 | 5 |
| h211 | simpleqa | no | no | yes | test | 8 | 17 | 0 |
| h212 | simpleqa | no | no | yes | test | 8 | 17 | 5 |
| h213 | science-chemistry | no | no | yes | calib | 9 | 8 | 2 |
| h214 | simpleqa | yes | yes | yes | test | 8 | 15 | 6 |
| h215 | simpleqa | yes | yes | yes | calib | 8 | 15 | 6 |
| h216 | claim | no | no | yes | calib | 9 | 17 | 0 |
| h217 | simpleqa | no | no | yes | calib | 9 | 21 | 3 |
| h218 | simpleqa | no | no | yes | calib | 8 | 15 | 1 |
| h219 | simpleqa | yes | no | **no** | test | 9 | 21 | 6 |
| h220 | claim | no | no | yes | calib | 9 | 10 | 1 |
| h221 | simpleqa | yes | no | **no** | test | 8 | 13 | 6 |
| h222 | simpleqa | yes | no | **no** | test | 11 | 24 | 8 |
| h223 | claim | no | no | yes | calib | 10 | 36 | 0 |
| h224 | claim | yes | yes | yes | calib | 11 | 27 | 0 |
| h225 | science-physics | yes | yes | yes | calib | 9 | 17 | 1 |
| h226 | simpleqa | yes | yes | yes | test | 9 | 21 | 6 |
| h227 | claim | yes | yes | yes | calib | 8 | 14 | 0 |
| h228 | simpleqa | no | no | yes | calib | 9 | 16 | 2 |
| h229 | science-physics | yes | no | **no** | test | 9 | 20 | 3 |
| h230 | simpleqa | no | no | yes | calib | 8 | 13 | 3 |
| h231 | simpleqa | no | no | yes | calib | 11 | 23 | 0 |
| h232 | simpleqa | no | no | yes | calib | 7 | 15 | 0 |
| h233 | science-physics | yes | yes | yes | calib | 9 | 26 | 0 |
| h234 | claim | yes | yes | yes | calib | 8 | 20 | 0 |
| h235 | simpleqa | no | no | yes | calib | 8 | 14 | 0 |
| h236 | claim | no | no | yes | calib | 9 | 17 | 0 |
| h237 | science-physics | yes | yes | yes | calib | 8 | 26 | 10 |
| h238 | science-chemistry | yes | no | **no** | test | 8 | 21 | 3 |
| h239 | science-chemistry | no | no | yes | calib | 9 | 21 | 0 |
| h240 | science-chemistry | no | no | yes | calib | 8 | 19 | 7 |
| h241 | science-chemistry | no | no | yes | test | 8 | 18 | 1 |
| h242 | claim | no | no | yes | calib | 9 | 18 | 0 |
| h243 | science-physics | no | no | yes | calib | 9 | 22 | 0 |
| h244 | science-physics | yes | yes | yes | calib | 8 | 26 | 0 |
| h245 | science-chemistry | no | no | yes | calib | 9 | 19 | 0 |
| h246 | claim | no | no | yes | calib | 9 | 36 | 0 |
| h247 | science-chemistry | yes | yes | yes | calib | 7 | 13 | 0 |
| h248 | science-chemistry | no | no | yes | calib | 9 | 23 | 7 |
| h249 | simpleqa | yes | yes | yes | calib | 10 | 19 | 4 |
| h250 | simpleqa | no | no | yes | calib | 6 | 11 | 0 |
| h251 | simpleqa | no | no | yes | calib | 9 | 26 | 0 |
| h252 | simpleqa | no | no | yes | test | 8 | 21 | 6 |
| h253 | science-chemistry | yes | no | **no** | test | 9 | 25 | 3 |
| h254 | simpleqa | no | no | yes | test | 8 | 25 | 0 |
| h255 | science-chemistry | no | no | yes | calib | 8 | 23 | 0 |
| h256 | simpleqa | yes | yes | yes | calib | 8 | 15 | 0 |
| h257 | science-physics | no | no | yes | calib | 9 | 25 | 7 |
| h258 | simpleqa | no | no | yes | test | 9 | 17 | 1 |
| h259 | claim | yes | yes | yes | test | 8 | 27 | 0 |
| h260 | simpleqa | yes | yes | yes | calib | 8 | 18 | 6 |
| h261 | simpleqa | yes | no | **no** | test | 8 | 20 | 4 |
| h262 | science-physics | no | yes | **no** | test | 10 | 30 | 0 |
| h263 | science-chemistry | no | no | yes | test | 10 | 32 | 5 |
| h264 | science-physics | yes | no | **no** | test | 8 | 17 | 3 |
| h265 | simpleqa | yes | yes | yes | calib | 9 | 23 | 10 |
| h266 | science-physics | no | no | yes | calib | 7 | 19 | 0 |
| h267 | science-chemistry | no | no | yes | calib | 9 | 23 | 0 |
| h268 | science-chemistry | yes | yes | yes | test | 9 | 18 | 0 |
| h269 | science-physics | yes | yes | yes | calib | 9 | 18 | 4 |
| h270 | science-chemistry | yes | yes | yes | calib | 10 | 27 | 10 |
| h271 | claim | no | no | yes | calib | 8 | 18 | 0 |
| h272 | science-chemistry | no | no | yes | calib | 8 | 19 | 0 |
| h273 | claim | yes | yes | yes | calib | 10 | 27 | 2 |
| h274 | claim | no | no | yes | calib | 9 | 14 | 0 |
| h275 | simpleqa | no | no | yes | calib | 9 | 18 | 0 |
| h276 | science-chemistry | no | no | yes | calib | 8 | 14 | 0 |
| h277 | science-chemistry | yes | no | **no** | test | 10 | 34 | 5 |
| h278 | science-chemistry | no | no | yes | calib | 9 | 24 | 5 |
| h279 | simpleqa | yes | no | **no** | test | 10 | 25 | 10 |
| h280 | simpleqa | no | no | yes | calib | 9 | 20 | 2 |
| h281 | simpleqa | yes | yes | yes | calib | 8 | 14 | 7 |
| h282 | science-physics | no | no | yes | test | 8 | 28 | 0 |
| h283 | science-physics | yes | no | **no** | test | 10 | 31 | 2 |
| h284 | science-chemistry | no | no | yes | calib | 8 | 21 | 0 |
| h285 | science-physics | no | no | yes | calib | 9 | 24 | 0 |
| h286 | claim | yes | yes | yes | calib | 10 | 20 | 7 |
| h287 | simpleqa | no | no | yes | calib | 8 | 19 | 4 |
| h288 | science-chemistry | yes | yes | yes | calib | 7 | 20 | 0 |
| h289 | simpleqa | no | no | yes | calib | 9 | 23 | 0 |
| h290 | claim | yes | yes | yes | calib | 9 | 16 | 0 |
| h291 | science-chemistry | yes | yes | yes | calib | 9 | 31 | 10 |
| h292 | simpleqa | no | no | yes | calib | 8 | 18 | 4 |
| h293 | simpleqa | yes | no | **no** | test | 8 | 13 | 6 |
| h294 | science-physics | no | no | yes | calib | 10 | 31 | 6 |
| h295 | claim | no | no | yes | calib | 9 | 21 | 0 |
| h296 | simpleqa | no | no | yes | test | 7 | 19 | 0 |
| h297 | simpleqa | yes | yes | yes | calib | 10 | 18 | 3 |
| h298 | science-chemistry | no | no | yes | calib | 9 | 19 | 0 |
| h299 | science-chemistry | yes | no | **no** | calib | 8 | 15 | 0 |
| h300 | claim | yes | yes | yes | test | 9 | 23 | 5 |

Wrong by category: claim 0/60, science-chemistry 11/60, science-physics 9/60, simpleqa 24/120


Wrong items:

- h004: Marc Julian Bradley, the first black Republican to serve in the Wisconsin Senate and only the second black Republican to serve in the Wisconsin Legislature, was born in 1981 and graduated from which high school? Is the answer "La Crosse Central High School"? (truth yes, model no)
- h013: Calculate the magnetic moment (μI) of a 13C nucleus.
Is the correct answer "9.1445 x 10^-27 J T-1"? (truth yes, model no)
- h018: What is the name of the university from which Thabo Cecil Makgoba, Chancellor of the University of the Western Cape in South Africa since 2012, first graduated with a PhD degree in 2009? Is the answer "University of Cape Town"? (truth yes, model no)
- h027: What is the surname of the individual who won the Applied Inorganic Chemistry Award in 2015? Is the answer "Lu"? (truth yes, model no)
- h039: The complementary color of blue is
Is the correct answer "yellow"? (truth yes, model no)
- h046: In which month and year was Firozabad district first established from Agra district in India? Is the answer "February 1989"? (truth yes, model no)
- h057: Calculate the density of the tightly coiled tropocollagen molecule, which may be considered to be a cylinder 2,800 \AA long and 14 \AA in diameter. It contains three poly-peptide chains of 1,000 amino acid residues each.
Is the correct answer "1.39 g/ cm^3"? (truth yes, model no)
- h058: What is the frequency of a 2-cm sound wave in sea water? What is the frequency of a 2-cm sound wave in sea water? The velocity of sound in sea water is \upsilon = 1.53 × 10^5 cm/sec.
Is the correct answer "76 kHz"? (truth yes, model no)
- h065: A converging lens of 5.0 cm focal length is used as a simple magnifier, producing a virtual image 25 cm from the eye. How far from the lens should the object be placed? What is the magnification?
Is the correct answer "4.2cm, 5.9"? (truth yes, model no)
- h075: How many children did Hank Williams have? Is the answer "2"? (truth yes, model no)
- h088: One of the major atmospheric pollutants emitted by fuel combustion power stations is a sulfur oxide mixture general-ly designated as S0_x. It consists mainly of SO_2 but may contain anywhere from 1 to 10% SO_3 computed as percent by weight of the total mass. What would be the approximate range to assign to x?
Is the correct answer "x = 3.14/1.56"? (truth yes, model no)
- h101: From which university did Louise M. Antony (American philosopher) receive her bachelor's degree in philosophy? Is the answer "Duke University"? (truth no, model yes)
- h102: In what year was the beetle species Glipa angustilineata described? Is the answer "1993"? (truth yes, model no)
- h103: A 20 gallon automobile gasoline tank is filled exactly to the top at 0°F just before the automobile is parked in a garage where the temperature is maintained at 70°F. How much gasoline is lost due to expansion as the car warms up? Assume the coefficient of volume expansion of gasoline to be .0012/°C.
Is the correct answer ".94 gal"? (truth yes, model no)
- h105: Calculate theCoulombicbarrier in the bombardment of ^209Bi Calculate theCoulombicbarrier in the bombardment of ^209Bi with alpha particles.
Is the correct answer "21.2MeV"? (truth yes, model no)
- h111: The planet Mercury travels around the Sun with a mean orbital radius of 5.8x10^10 m. The mass of the Sun is 1.99x10^30 kg. Use Newton's version of Kepler's third law to determine how long it takes Mercury to orbit the Sun. Give your answer in Earth days.
Is the correct answer "88.3"? (truth yes, model no)
- h112: What college did Anna Moriah Wilson graduate from in 2014? Is the answer "Emory & Henry College"? (truth no, model yes)
- h115: To whom did Ragnar say, "When everyone wanted you dead, I kept you alive" in the Vikings episode "The Profit and the Loss"? Is the answer "Rollo"? (truth yes, model no)
- h127: What was the original name of the show that conductor David Randolph hosted on the radio station WNYC? Is the answer "Music for the Connoisseur"? (truth yes, model no)
- h135: A sample of bristle cone pine wood of age 7,000 \pm 100 years, known by counting growth rings, possesses an activity of 6.6 d(disintegrations) / minute-g of carbon. Calculate the exact age of the wood sample from radiochemical evidence.
Is the correct answer "6,225 years old"? (truth yes, model no)
- h137: How many papers did Kunihiko Kodaira publish by 1941? Is the answer "10"? (truth yes, model no)
- h138: Consider the reaction I_2 \rightarrow 2I at 1000°K and 1 atm. The fundamental vibration frequency ѵof I_2 is 214.4 cm^-1, and the internuclear distance is 0.2667 nm. Calculate the equilibrium constant K_P for the reaction if the ground state of I is a doublet ^2P_3/2,1/2 With a separation of 7603 cm^-1 . The dissociation energy of I_2 is 1.542 eV.
Is the correct answer "1.571 × 10^-3"? (truth yes, model no)
- h140: What battery does the G-Shock GG-B100-8A come with? Is the answer "CR2025"? (truth yes, model no)
- h152: What was the last year Charles Boyle, Viscount Dungarvan, 3rd Baron Clifford, was Member of Parliament for Tamworth in the British House of Commons? Is the answer "1679"? (truth yes, model no)
- h159: Predict the number of lines in the EPR spectrum of a solution of dimethylnitroxide (CH3)2NO• assuming the lines do not overlap.
Is the correct answer "3"? (truth yes, model no)
- h190: What is the name of the organization to which the Society of Illustrators sold the rights to their Illustrator Show skits in 1925? Is the answer "Vice & Virtue"? (truth no, model yes)
- h191: Who won the 1991 Ig Nobel Prize for Peace? Is the answer "Patricia Mary Edmondson"? (truth no, model yes)
- h194: What were the month, day, and year that Thomas Randolph wrote to the Earl of Leicester, stating that he was unable and unwilling to commit his opinions on Mary's actions on paper for fear of appearing "malicieus foolyshe and unadvised"? Is the answer "14 February 1566"? (truth yes, model no)
- h197: Between what dates was the Stanford University exhibition titled "Sam Richardson: Islands, Ice, and Sand" on view? Please give me the full dates (month, date, and year). Is the answer "23 September, 2021 to 13 March, 2022"? (truth yes, model no)
- h204: In what month and year was the Flitzer on Surfside Pier retired? Is the answer "September 2018"? (truth yes, model no)
- h219: Which Indian state is also known as Veer Bhumi? Is the answer "Himachal Pradesh"? (truth yes, model no)
- h221: How many years was the scholarship that Mary Fairchild MacMonnies Low won from the St. Louis School of Fine Arts for? Is the answer "three"? (truth yes, model no)
- h222: What was the release price for the Sonic Free Riders original soundtrack in Japan in Japanese Yen? Is the answer "1800 JPY"? (truth yes, model no)
- h229: A house near a lake is kept warm by a heat engine. In winter, water from beneath the ice covering the lake is pumped through the heat engine. Heat is extracted until the water is on the point of freezing when it is ejected. The outside air is used as a sink. Assume that the air temperature is -15 °C and the temperature of the water from the lake is 2°C. Calculate the rate at which water must be pumped to the engine. The efficiency of the engine is one-fifth that of a Carnot engine and the house requires 10 kW.
Is the correct answer "102.4 liters/s"? (truth yes, model no)
- h238: A chemical reaction takes place in a container of cross-sectional area $50 \mathrm{~cm}^2$. As a result of the reaction, a piston is pushed out through $15 \mathrm{~cm}$ against an external pressure of $1.0 \mathrm{~atm}$. Calculate the work done by the system.
Is the correct answer "-75 $\mathrm{~J}$"? (truth yes, model no)
- h253: A particle of mass $1.0 \mathrm{~g}$ is released near the surface of the Earth, where the acceleration of free fall is $g=8.91 \mathrm{~m} \mathrm{~s}^{-2}$. What will be its kinetic energy after  $1.0 \mathrm{~s}$. Ignore air resistance?
Is the correct answer "48 $\mathrm{~mJ}$"? (truth yes, model no)
- h261: On what date did the last total lunar eclipse for three years occur? Is the answer "November 8, 2022"? (truth yes, model no)
- h262: A math book and a physics book sitting on a table are tied together with a length of string. With the string taut one book is pushed off the edge of the table. As it falls the other book is dragged horizontally across the table surface. With no friction acceleration of the books is
Is the correct answer "dependent on the weight of the books"? (truth no, model yes)
- h264: An airplane is flying at Mach 1.75 at an altitude of 8000 m, where the speed of sound is How long after the plane passes directly overhead will you hear the sonic boom? (Unit: m/s)
Is the correct answer "560"? (truth yes, model no)
- h277: Carbon dioxide is reduced by hydrogen according to the equation CO_2(g) + H_2(g) \rightleftarrows CO(g) + H_2O(g) . One mole of CO_2 is reacted with one mole of H_2 at 825K and it is found that, at equilibrium, 0.27atmof CO is present. Determine the equilibrium constant, K, at 825K .
Is the correct answer "0.137"? (truth yes, model no)
- h279: In the 2012 research paper titled "Multiplication of EEG Samples through Replicating, Biasing, and Overlapping" by Adham Atyabi et al., between what frequencies was the EEG dataset bandpass filtered, in hertz (Hz)? Is the answer "1 & 50"? (truth yes, model no)
- h283: Ordinary light is incident on a pile of eight glass plates at the polarizing angle. If the index of refraction of each plate, n, is 1.75, find the percentage polarization of the light transmitted.
Is the correct answer "73.5%"? (truth yes, model no)
- h293: In which year was the Kangri cancer effect first studied? Is the answer "1866"? (truth yes, model no)
- h299: The maximum weekly dose for the hands and forearms, as-suming a mass of 6kg and a surface area of 950 cm^2, is 2.0 rem. How long would it take for a person to receive this dose from a 15millicuriesource emitting a 3.0MeVgamma ray? The distance between the source and the receiving surface is 15 cm. Assume no radiation is absorbed by the air.
Is the correct answer "22.6 min"? (truth yes, model no)
