# Pool run 4: base `claude-sonnet-5-5` (effort default, adaptive thinking)

299 questions processed; 1 hit the 16,000-token cap, gave no FINAL ANSWER or failed claim extraction, and are excluded; base model wrong on **30** of 298 answered. API cost $4.0667. Contentions are the claims in the visible answer (DEVIATIONS.md, D1–D3).

Test set rule: D6: all wrong items (at most 40, at random) + an equal number of right items at random (seed 2026). Test set: 30 wrong + 30 right. Calibration pool: 238 items.

| id | category | truth | model | correct | set | contentions | related pairs | contradictions |
|---|---|---|---|---|---|---|---|---|
| h001 | simpleqa | yes | yes | yes | calib | 9 | 15 | 4 |
| h002 | claim | yes | yes | yes | calib | 10 | 25 | 0 |
| h003 | simpleqa | no | no | yes | calib | 9 | 12 | 1 |
| h004 | simpleqa | yes | no | **no** | test | 8 | 18 | 5 |
| h005 | simpleqa | yes | no | **no** | test | 10 | 16 | 6 |
| h006 | claim | no | no | yes | calib | 11 | 34 | 9 |
| h007 | science-chemistry | no | no | yes | calib | 8 | 28 | 0 |
| h008 | claim | yes | yes | yes | calib | 12 | 31 | 5 |
| h009 | claim | yes | yes | yes | calib | 11 | 27 | 13 |
| h010 | claim | no | no | yes | calib | 11 | 30 | 6 |
| h011 | claim | no | no | yes | calib | 10 | 27 | 1 |
| h012 | simpleqa | yes | yes | yes | calib | 9 | 18 | 6 |
| h013 | science-chemistry | yes | no | **no** | test | 9 | 26 | 0 |
| h014 | science-chemistry | yes | no | **no** | test | 8 | 24 | 11 |
| h015 | science-chemistry | yes | yes | yes | calib | 10 | 38 | 12 |
| h016 | simpleqa | no | no | yes | calib | 10 | 23 | 1 |
| h017 | science-chemistry | yes | yes | yes | test | 10 | 29 | 0 |
| h018 | simpleqa | yes | (extractor returned 1 claims) | — | excluded | | | |
| h019 | science-chemistry | yes | yes | yes | calib | 10 | 13 | 5 |
| h020 | science-chemistry | no | no | yes | calib | 10 | 16 | 0 |
| h021 | claim | yes | yes | yes | calib | 10 | 22 | 1 |
| h022 | claim | yes | yes | yes | calib | 9 | 22 | 0 |
| h023 | simpleqa | no | no | yes | calib | 9 | 13 | 0 |
| h024 | science-physics | yes | yes | yes | calib | 9 | 17 | 5 |
| h025 | simpleqa | yes | yes | yes | calib | 11 | 29 | 6 |
| h026 | simpleqa | yes | yes | yes | calib | 9 | 13 | 4 |
| h027 | simpleqa | yes | no | **no** | test | 9 | 18 | 5 |
| h028 | science-physics | no | no | yes | calib | 7 | 12 | 0 |
| h029 | claim | no | no | yes | calib | 7 | 6 | 0 |
| h030 | science-physics | no | no | yes | test | 8 | 23 | 0 |
| h031 | science-physics | no | no | yes | calib | 9 | 23 | 0 |
| h032 | science-physics | no | no | yes | calib | 8 | 19 | 0 |
| h033 | claim | yes | yes | yes | calib | 9 | 22 | 7 |
| h034 | science-physics | yes | yes | yes | calib | 8 | 21 | 0 |
| h035 | science-physics | no | no | yes | calib | 9 | 26 | 0 |
| h036 | simpleqa | no | no | yes | test | 9 | 15 | 0 |
| h037 | science-physics | yes | yes | yes | calib | 10 | 36 | 0 |
| h038 | science-chemistry | no | no | yes | calib | 8 | 15 | 0 |
| h039 | science-physics | yes | yes | yes | calib | 9 | 28 | 15 |
| h040 | simpleqa | no | no | yes | calib | 9 | 29 | 0 |
| h041 | claim | no | no | yes | calib | 9 | 19 | 10 |
| h042 | science-chemistry | no | no | yes | calib | 7 | 19 | 5 |
| h043 | science-physics | no | no | yes | calib | 8 | 21 | 1 |
| h044 | simpleqa | no | no | yes | calib | 8 | 23 | 0 |
| h045 | claim | no | no | yes | calib | 10 | 12 | 1 |
| h046 | simpleqa | yes | yes | yes | test | 10 | 23 | 7 |
| h047 | simpleqa | yes | yes | yes | calib | 10 | 34 | 12 |
| h048 | science-chemistry | yes | yes | yes | calib | 9 | 25 | 8 |
| h049 | science-physics | no | no | yes | calib | 9 | 26 | 0 |
| h050 | science-chemistry | yes | yes | yes | calib | 7 | 21 | 0 |
| h051 | science-physics | yes | yes | yes | calib | 9 | 28 | 6 |
| h052 | science-chemistry | no | no | yes | test | 8 | 28 | 0 |
| h053 | simpleqa | yes | yes | yes | calib | 10 | 27 | 11 |
| h054 | simpleqa | no | no | yes | calib | 8 | 13 | 1 |
| h055 | simpleqa | yes | yes | yes | calib | 9 | 14 | 4 |
| h056 | simpleqa | yes | yes | yes | calib | 9 | 18 | 1 |
| h057 | science-chemistry | yes | no | **no** | test | 9 | 21 | 0 |
| h058 | science-physics | yes | yes | yes | calib | 8 | 24 | 8 |
| h059 | science-physics | yes | yes | yes | calib | 9 | 25 | 7 |
| h060 | claim | yes | yes | yes | calib | 8 | 11 | 0 |
| h061 | simpleqa | yes | yes | yes | calib | 10 | 19 | 3 |
| h062 | science-physics | no | no | yes | calib | 10 | 29 | 0 |
| h063 | simpleqa | yes | yes | yes | calib | 9 | 28 | 7 |
| h064 | science-physics | yes | yes | yes | calib | 10 | 28 | 0 |
| h065 | science-physics | yes | no | **no** | test | 8 | 18 | 3 |
| h066 | science-physics | yes | yes | yes | calib | 7 | 16 | 4 |
| h067 | simpleqa | no | no | yes | calib | 9 | 20 | 0 |
| h068 | claim | yes | yes | yes | calib | 10 | 18 | 7 |
| h069 | claim | yes | yes | yes | calib | 8 | 9 | 0 |
| h070 | science-physics | yes | yes | yes | calib | 8 | 14 | 2 |
| h071 | claim | no | no | yes | calib | 9 | 9 | 0 |
| h072 | claim | no | no | yes | calib | 10 | 31 | 6 |
| h073 | claim | no | no | yes | calib | 10 | 16 | 0 |
| h074 | simpleqa | no | no | yes | calib | 8 | 13 | 1 |
| h075 | simpleqa | yes | yes | yes | calib | 10 | 25 | 3 |
| h076 | claim | yes | yes | yes | calib | 9 | 19 | 1 |
| h077 | science-physics | yes | yes | yes | calib | 7 | 12 | 0 |
| h078 | science-chemistry | yes | yes | yes | calib | 7 | 21 | 0 |
| h079 | science-physics | no | no | yes | calib | 9 | 33 | 4 |
| h080 | claim | yes | yes | yes | calib | 10 | 23 | 6 |
| h081 | science-physics | no | no | yes | test | 9 | 21 | 0 |
| h082 | simpleqa | yes | yes | yes | calib | 8 | 16 | 6 |
| h083 | simpleqa | no | no | yes | calib | 13 | 24 | 6 |
| h084 | simpleqa | no | no | yes | calib | 9 | 17 | 0 |
| h085 | simpleqa | no | no | yes | calib | 9 | 20 | 14 |
| h086 | simpleqa | no | no | yes | calib | 10 | 20 | 6 |
| h087 | claim | yes | yes | yes | calib | 9 | 22 | 1 |
| h088 | science-chemistry | yes | no | **no** | test | 8 | 18 | 0 |
| h089 | simpleqa | yes | yes | yes | calib | 8 | 15 | 7 |
| h090 | claim | yes | yes | yes | calib | 10 | 24 | 1 |
| h091 | claim | no | no | yes | calib | 11 | 30 | 12 |
| h092 | science-physics | yes | yes | yes | calib | 10 | 23 | 5 |
| h093 | science-chemistry | yes | no | **no** | test | 11 | 44 | 14 |
| h094 | simpleqa | yes | yes | yes | calib | 9 | 20 | 7 |
| h095 | claim | yes | yes | yes | calib | 10 | 29 | 6 |
| h096 | simpleqa | yes | no | **no** | test | 9 | 23 | 6 |
| h097 | claim | no | no | yes | calib | 11 | 26 | 1 |
| h098 | claim | no | no | yes | calib | 8 | 15 | 0 |
| h099 | simpleqa | yes | yes | yes | calib | 9 | 17 | 6 |
| h100 | simpleqa | no | no | yes | calib | 8 | 17 | 0 |
| h102 | simpleqa | yes | no | **no** | test | 8 | 20 | 9 |
| h103 | science-physics | yes | no | **no** | test | 9 | 24 | 5 |
| h104 | claim | yes | yes | yes | calib | 11 | 16 | 0 |
| h105 | science-chemistry | yes | yes | yes | calib | 9 | 18 | 2 |
| h106 | simpleqa | no | no | yes | calib | 8 | 15 | 0 |
| h107 | science-chemistry | no | no | yes | calib | 9 | 20 | 1 |
| h108 | science-chemistry | no | no | yes | test | 8 | 19 | 0 |
| h109 | simpleqa | no | no | yes | test | 9 | 22 | 4 |
| h110 | simpleqa | yes | yes | yes | calib | 9 | 30 | 13 |
| h111 | science-physics | yes | no | **no** | test | 9 | 24 | 8 |
| h112 | simpleqa | no | no | yes | calib | 8 | 12 | 0 |
| h113 | science-physics | yes | yes | yes | calib | 10 | 31 | 8 |
| h114 | claim | no | no | yes | calib | 9 | 22 | 0 |
| h115 | simpleqa | yes | no | **no** | test | 10 | 25 | 9 |
| h116 | simpleqa | no | no | yes | calib | 8 | 10 | 1 |
| h117 | claim | no | no | yes | calib | 9 | 18 | 1 |
| h118 | science-chemistry | no | no | yes | calib | 9 | 27 | 1 |
| h119 | science-physics | yes | yes | yes | test | 9 | 32 | 11 |
| h120 | science-physics | no | no | yes | calib | 8 | 19 | 5 |
| h121 | simpleqa | yes | yes | yes | calib | 10 | 36 | 12 |
| h122 | science-chemistry | yes | yes | yes | calib | 10 | 34 | 0 |
| h123 | simpleqa | yes | yes | yes | calib | 10 | 31 | 0 |
| h124 | claim | yes | yes | yes | calib | 9 | 8 | 0 |
| h125 | science-physics | no | no | yes | test | 7 | 18 | 3 |
| h126 | science-physics | yes | yes | yes | calib | 9 | 24 | 5 |
| h127 | simpleqa | yes | yes | yes | calib | 8 | 13 | 4 |
| h128 | simpleqa | yes | yes | yes | calib | 10 | 31 | 7 |
| h129 | science-physics | no | no | yes | calib | 9 | 19 | 0 |
| h130 | science-physics | yes | yes | yes | calib | 8 | 21 | 0 |
| h131 | claim | no | no | yes | calib | 9 | 21 | 0 |
| h132 | claim | no | no | yes | calib | 10 | 18 | 1 |
| h133 | simpleqa | no | no | yes | calib | 7 | 7 | 0 |
| h134 | simpleqa | no | no | yes | calib | 10 | 23 | 0 |
| h135 | science-chemistry | yes | no | **no** | test | 8 | 22 | 1 |
| h136 | science-chemistry | yes | yes | yes | test | 9 | 20 | 8 |
| h137 | simpleqa | yes | yes | yes | calib | 9 | 19 | 9 |
| h138 | science-chemistry | yes | no | **no** | test | 10 | 18 | 3 |
| h139 | simpleqa | no | no | yes | calib | 11 | 26 | 0 |
| h140 | simpleqa | yes | no | **no** | test | 8 | 14 | 4 |
| h141 | simpleqa | no | no | yes | calib | 9 | 18 | 0 |
| h142 | simpleqa | yes | yes | yes | calib | 8 | 9 | 3 |
| h143 | simpleqa | no | no | yes | calib | 8 | 15 | 0 |
| h144 | simpleqa | no | no | yes | calib | 10 | 33 | 4 |
| h145 | simpleqa | yes | yes | yes | calib | 9 | 16 | 5 |
| h146 | science-chemistry | yes | yes | yes | calib | 9 | 26 | 0 |
| h147 | science-physics | no | no | yes | test | 10 | 23 | 6 |
| h148 | claim | no | no | yes | calib | 10 | 19 | 0 |
| h149 | simpleqa | yes | yes | yes | test | 9 | 15 | 4 |
| h150 | simpleqa | yes | yes | yes | calib | 10 | 22 | 6 |
| h151 | simpleqa | no | no | yes | calib | 9 | 22 | 0 |
| h152 | simpleqa | yes | no | **no** | test | 9 | 13 | 4 |
| h153 | science-chemistry | no | no | yes | calib | 8 | 17 | 0 |
| h154 | science-chemistry | no | no | yes | calib | 9 | 19 | 1 |
| h155 | claim | yes | yes | yes | calib | 12 | 26 | 10 |
| h156 | science-chemistry | no | no | yes | calib | 8 | 20 | 0 |
| h157 | science-physics | no | no | yes | calib | 9 | 24 | 4 |
| h158 | claim | yes | yes | yes | calib | 10 | 45 | 9 |
| h159 | science-chemistry | yes | no | **no** | test | 9 | 20 | 6 |
| h160 | science-chemistry | yes | yes | yes | calib | 8 | 21 | 0 |
| h161 | science-physics | no | no | yes | calib | 9 | 29 | 9 |
| h162 | simpleqa | no | no | yes | calib | 9 | 26 | 3 |
| h163 | simpleqa | no | no | yes | test | 9 | 15 | 4 |
| h164 | science-chemistry | yes | yes | yes | calib | 9 | 22 | 3 |
| h165 | science-chemistry | no | no | yes | calib | 9 | 16 | 4 |
| h166 | simpleqa | yes | yes | yes | calib | 8 | 13 | 5 |
| h167 | science-physics | no | no | yes | calib | 10 | 17 | 1 |
| h168 | science-physics | no | no | yes | calib | 8 | 15 | 0 |
| h169 | science-physics | no | no | yes | test | 8 | 19 | 0 |
| h170 | simpleqa | yes | yes | yes | calib | 10 | 14 | 0 |
| h171 | simpleqa | yes | yes | yes | test | 8 | 16 | 2 |
| h172 | science-physics | no | no | yes | calib | 10 | 19 | 0 |
| h173 | simpleqa | no | no | yes | calib | 9 | 24 | 13 |
| h174 | simpleqa | no | no | yes | calib | 9 | 18 | 0 |
| h175 | science-chemistry | no | no | yes | calib | 8 | 20 | 0 |
| h176 | science-chemistry | no | no | yes | calib | 9 | 25 | 3 |
| h177 | simpleqa | no | no | yes | calib | 10 | 19 | 0 |
| h178 | simpleqa | no | no | yes | calib | 9 | 25 | 7 |
| h179 | claim | no | no | yes | calib | 10 | 23 | 0 |
| h180 | science-physics | no | no | yes | test | 9 | 18 | 3 |
| h181 | science-physics | no | no | yes | calib | 7 | 18 | 6 |
| h182 | claim | yes | yes | yes | calib | 10 | 20 | 3 |
| h183 | claim | no | no | yes | calib | 8 | 16 | 2 |
| h184 | science-physics | no | no | yes | calib | 8 | 20 | 0 |
| h185 | simpleqa | no | no | yes | calib | 10 | 17 | 0 |
| h186 | simpleqa | no | no | yes | calib | 8 | 8 | 0 |
| h187 | simpleqa | yes | yes | yes | calib | 8 | 16 | 7 |
| h188 | claim | yes | yes | yes | calib | 10 | 17 | 0 |
| h189 | simpleqa | no | no | yes | calib | 8 | 15 | 0 |
| h190 | simpleqa | no | no | yes | calib | 9 | 17 | 5 |
| h191 | simpleqa | no | no | yes | calib | 6 | 11 | 0 |
| h192 | science-physics | yes | yes | yes | calib | 8 | 15 | 0 |
| h193 | simpleqa | yes | yes | yes | calib | 9 | 20 | 3 |
| h194 | simpleqa | yes | no | **no** | test | 8 | 12 | 3 |
| h195 | claim | yes | yes | yes | calib | 10 | 27 | 0 |
| h196 | claim | no | no | yes | calib | 10 | 23 | 0 |
| h197 | simpleqa | yes | yes | yes | test | 10 | 26 | 8 |
| h198 | simpleqa | yes | yes | yes | calib | 8 | 19 | 3 |
| h199 | simpleqa | no | no | yes | calib | 8 | 17 | 7 |
| h200 | science-chemistry | no | no | yes | calib | 8 | 24 | 0 |
| h201 | simpleqa | yes | yes | yes | test | 9 | 12 | 6 |
| h202 | simpleqa | no | no | yes | calib | 9 | 22 | 0 |
| h203 | science-physics | yes | yes | yes | calib | 10 | 23 | 9 |
| h204 | simpleqa | yes | yes | yes | test | 8 | 16 | 8 |
| h205 | science-chemistry | no | no | yes | test | 10 | 23 | 8 |
| h206 | simpleqa | no | no | yes | calib | 9 | 13 | 4 |
| h207 | science-chemistry | yes | yes | yes | calib | 8 | 17 | 0 |
| h208 | claim | no | no | yes | calib | 8 | 18 | 0 |
| h209 | claim | yes | yes | yes | calib | 9 | 14 | 6 |
| h210 | science-physics | yes | yes | yes | calib | 9 | 24 | 8 |
| h211 | simpleqa | no | no | yes | calib | 9 | 25 | 8 |
| h212 | simpleqa | no | no | yes | calib | 8 | 12 | 4 |
| h213 | science-chemistry | no | no | yes | calib | 8 | 8 | 0 |
| h214 | simpleqa | yes | yes | yes | calib | 8 | 13 | 3 |
| h215 | simpleqa | yes | yes | yes | test | 9 | 11 | 3 |
| h216 | claim | no | no | yes | calib | 9 | 20 | 0 |
| h217 | simpleqa | no | no | yes | calib | 8 | 15 | 1 |
| h218 | simpleqa | no | no | yes | calib | 9 | 22 | 0 |
| h219 | simpleqa | yes | yes | yes | calib | 10 | 33 | 18 |
| h220 | claim | no | no | yes | calib | 9 | 17 | 2 |
| h221 | simpleqa | yes | yes | yes | calib | 9 | 15 | 6 |
| h222 | simpleqa | yes | no | **no** | test | 7 | 9 | 3 |
| h223 | claim | no | no | yes | calib | 10 | 26 | 1 |
| h224 | claim | yes | yes | yes | calib | 9 | 18 | 6 |
| h225 | science-physics | yes | yes | yes | calib | 7 | 13 | 0 |
| h226 | simpleqa | yes | yes | yes | calib | 9 | 16 | 4 |
| h227 | claim | yes | yes | yes | calib | 10 | 13 | 4 |
| h228 | simpleqa | no | no | yes | calib | 10 | 16 | 4 |
| h229 | science-physics | yes | yes | yes | test | 10 | 37 | 0 |
| h230 | simpleqa | no | no | yes | calib | 8 | 12 | 0 |
| h231 | simpleqa | no | no | yes | calib | 10 | 24 | 0 |
| h232 | simpleqa | no | no | yes | calib | 11 | 22 | 0 |
| h233 | science-physics | yes | yes | yes | calib | 9 | 20 | 3 |
| h234 | claim | yes | yes | yes | calib | 10 | 22 | 0 |
| h235 | simpleqa | no | no | yes | calib | 10 | 19 | 5 |
| h236 | claim | no | no | yes | calib | 9 | 18 | 0 |
| h237 | science-physics | yes | no | **no** | test | 9 | 20 | 14 |
| h238 | science-chemistry | yes | no | **no** | test | 9 | 27 | 8 |
| h239 | science-chemistry | no | no | yes | calib | 10 | 17 | 0 |
| h240 | science-chemistry | no | no | yes | calib | 8 | 27 | 7 |
| h241 | science-chemistry | no | no | yes | calib | 9 | 22 | 3 |
| h242 | claim | no | no | yes | calib | 9 | 13 | 0 |
| h243 | science-physics | no | no | yes | test | 9 | 24 | 4 |
| h244 | science-physics | yes | yes | yes | calib | 9 | 26 | 0 |
| h245 | science-chemistry | no | no | yes | calib | 9 | 24 | 0 |
| h246 | claim | no | no | yes | calib | 9 | 32 | 0 |
| h247 | science-chemistry | yes | yes | yes | calib | 7 | 14 | 0 |
| h248 | science-chemistry | no | no | yes | test | 7 | 17 | 1 |
| h249 | simpleqa | yes | no | **no** | test | 9 | 14 | 7 |
| h250 | simpleqa | no | no | yes | calib | 11 | 29 | 5 |
| h251 | simpleqa | no | no | yes | calib | 9 | 25 | 0 |
| h252 | simpleqa | no | no | yes | calib | 9 | 11 | 0 |
| h253 | science-chemistry | yes | no | **no** | test | 8 | 19 | 9 |
| h254 | simpleqa | no | no | yes | calib | 9 | 18 | 0 |
| h255 | science-chemistry | no | no | yes | calib | 8 | 22 | 0 |
| h256 | simpleqa | yes | yes | yes | test | 10 | 22 | 9 |
| h257 | science-physics | no | no | yes | calib | 10 | 16 | 10 |
| h258 | simpleqa | no | no | yes | calib | 7 | 13 | 4 |
| h259 | claim | yes | yes | yes | calib | 9 | 15 | 1 |
| h260 | simpleqa | yes | yes | yes | calib | 10 | 26 | 2 |
| h261 | simpleqa | yes | yes | yes | calib | 8 | 25 | 2 |
| h262 | science-physics | no | yes | **no** | test | 10 | 25 | 5 |
| h263 | science-chemistry | no | no | yes | test | 8 | 15 | 3 |
| h264 | science-physics | yes | no | **no** | test | 10 | 28 | 6 |
| h265 | simpleqa | yes | yes | yes | calib | 9 | 25 | 12 |
| h266 | science-physics | no | no | yes | calib | 8 | 23 | 0 |
| h267 | science-chemistry | no | no | yes | calib | 10 | 17 | 2 |
| h268 | science-chemistry | yes | yes | yes | calib | 10 | 20 | 1 |
| h269 | science-physics | yes | yes | yes | calib | 9 | 19 | 0 |
| h270 | science-chemistry | yes | yes | yes | calib | 8 | 23 | 7 |
| h271 | claim | no | no | yes | calib | 9 | 18 | 1 |
| h272 | science-chemistry | no | no | yes | calib | 8 | 18 | 0 |
| h273 | claim | yes | yes | yes | calib | 11 | 38 | 18 |
| h274 | claim | no | no | yes | calib | 9 | 19 | 5 |
| h275 | simpleqa | no | no | yes | calib | 8 | 19 | 0 |
| h276 | science-chemistry | no | no | yes | calib | 10 | 40 | 7 |
| h277 | science-chemistry | yes | no | **no** | test | 9 | 29 | 4 |
| h278 | science-chemistry | no | no | yes | calib | 10 | 18 | 0 |
| h279 | simpleqa | yes | no | **no** | test | 8 | 21 | 8 |
| h280 | simpleqa | no | no | yes | calib | 10 | 6 | 0 |
| h281 | simpleqa | yes | yes | yes | test | 8 | 12 | 6 |
| h282 | science-physics | no | no | yes | calib | 9 | 26 | 10 |
| h283 | science-physics | yes | yes | yes | calib | 10 | 27 | 6 |
| h284 | science-chemistry | no | no | yes | calib | 9 | 22 | 2 |
| h285 | science-physics | no | no | yes | calib | 9 | 19 | 0 |
| h286 | claim | yes | yes | yes | calib | 8 | 10 | 0 |
| h287 | simpleqa | no | no | yes | calib | 9 | 18 | 0 |
| h288 | science-chemistry | yes | yes | yes | calib | 8 | 20 | 0 |
| h289 | simpleqa | no | no | yes | calib | 9 | 24 | 1 |
| h290 | claim | yes | yes | yes | calib | 10 | 17 | 2 |
| h291 | science-chemistry | yes | yes | yes | calib | 10 | 38 | 0 |
| h292 | simpleqa | no | no | yes | test | 9 | 12 | 0 |
| h293 | simpleqa | yes | yes | yes | calib | 10 | 16 | 8 |
| h294 | science-physics | no | yes | **no** | test | 10 | 18 | 4 |
| h295 | claim | no | no | yes | test | 9 | 15 | 0 |
| h296 | simpleqa | no | no | yes | calib | 8 | 18 | 0 |
| h297 | simpleqa | yes | yes | yes | calib | 8 | 12 | 6 |
| h298 | science-chemistry | no | no | yes | calib | 8 | 14 | 0 |
| h299 | science-chemistry | yes | yes | yes | calib | 10 | 21 | 5 |
| h300 | claim | yes | yes | yes | calib | 9 | 23 | 0 |

Wrong by category: claim 0/60, science-chemistry 11/60, science-physics 7/60, simpleqa 12/118


Wrong items:

- h004: Marc Julian Bradley, the first black Republican to serve in the Wisconsin Senate and only the second black Republican to serve in the Wisconsin Legislature, was born in 1981 and graduated from which high school? Is the answer "La Crosse Central High School"? (truth yes, model no)
- h005: What position did the album "Different World" by Alan Walker land in the year-end 2019 US Top Dance/Electronic Albums (Billboard)? Is the answer "7"? (truth yes, model no)
- h013: Calculate the magnetic moment (μI) of a 13C nucleus.
Is the correct answer "9.1445 x 10^-27 J T-1"? (truth yes, model no)
- h014: A student made three successiveweighingsof an object as follows: 9.17 g, 9.15 g, and 9.20 g. What is the average weight of the object in milligrams?
Is the correct answer "9170 mg"? (truth yes, model no)
- h027: What is the surname of the individual who won the Applied Inorganic Chemistry Award in 2015? Is the answer "Lu"? (truth yes, model no)
- h057: Calculate the density of the tightly coiled tropocollagen molecule, which may be considered to be a cylinder 2,800 \AA long and 14 \AA in diameter. It contains three poly-peptide chains of 1,000 amino acid residues each.
Is the correct answer "1.39 g/ cm^3"? (truth yes, model no)
- h065: A converging lens of 5.0 cm focal length is used as a simple magnifier, producing a virtual image 25 cm from the eye. How far from the lens should the object be placed? What is the magnification?
Is the correct answer "4.2cm, 5.9"? (truth yes, model no)
- h088: One of the major atmospheric pollutants emitted by fuel combustion power stations is a sulfur oxide mixture general-ly designated as S0_x. It consists mainly of SO_2 but may contain anywhere from 1 to 10% SO_3 computed as percent by weight of the total mass. What would be the approximate range to assign to x?
Is the correct answer "x = 3.14/1.56"? (truth yes, model no)
- h093: Your supervisor asks you to determine the enthalpy of a certain chemical reaction. Which would you do?
Is the correct answer "Use a solution calorimeter such as a coffee-cup calorimeter to measure the heat."? (truth yes, model no)
- h096: In what position did Romania finish in the 2022 Rugby Europe Championship? Is the answer "Second position"? (truth yes, model no)
- h102: In what year was the beetle species Glipa angustilineata described? Is the answer "1993"? (truth yes, model no)
- h103: A 20 gallon automobile gasoline tank is filled exactly to the top at 0°F just before the automobile is parked in a garage where the temperature is maintained at 70°F. How much gasoline is lost due to expansion as the car warms up? Assume the coefficient of volume expansion of gasoline to be .0012/°C.
Is the correct answer ".94 gal"? (truth yes, model no)
- h111: The planet Mercury travels around the Sun with a mean orbital radius of 5.8x10^10 m. The mass of the Sun is 1.99x10^30 kg. Use Newton's version of Kepler's third law to determine how long it takes Mercury to orbit the Sun. Give your answer in Earth days.
Is the correct answer "88.3"? (truth yes, model no)
- h115: To whom did Ragnar say, "When everyone wanted you dead, I kept you alive" in the Vikings episode "The Profit and the Loss"? Is the answer "Rollo"? (truth yes, model no)
- h135: A sample of bristle cone pine wood of age 7,000 \pm 100 years, known by counting growth rings, possesses an activity of 6.6 d(disintegrations) / minute-g of carbon. Calculate the exact age of the wood sample from radiochemical evidence.
Is the correct answer "6,225 years old"? (truth yes, model no)
- h138: Consider the reaction I_2 \rightarrow 2I at 1000°K and 1 atm. The fundamental vibration frequency ѵof I_2 is 214.4 cm^-1, and the internuclear distance is 0.2667 nm. Calculate the equilibrium constant K_P for the reaction if the ground state of I is a doublet ^2P_3/2,1/2 With a separation of 7603 cm^-1 . The dissociation energy of I_2 is 1.542 eV.
Is the correct answer "1.571 × 10^-3"? (truth yes, model no)
- h140: What battery does the G-Shock GG-B100-8A come with? Is the answer "CR2025"? (truth yes, model no)
- h152: What was the last year Charles Boyle, Viscount Dungarvan, 3rd Baron Clifford, was Member of Parliament for Tamworth in the British House of Commons? Is the answer "1679"? (truth yes, model no)
- h159: Predict the number of lines in the EPR spectrum of a solution of dimethylnitroxide (CH3)2NO• assuming the lines do not overlap.
Is the correct answer "3"? (truth yes, model no)
- h194: What were the month, day, and year that Thomas Randolph wrote to the Earl of Leicester, stating that he was unable and unwilling to commit his opinions on Mary's actions on paper for fear of appearing "malicieus foolyshe and unadvised"? Is the answer "14 February 1566"? (truth yes, model no)
- h222: What was the release price for the Sonic Free Riders original soundtrack in Japan in Japanese Yen? Is the answer "1800 JPY"? (truth yes, model no)
- h237: Calculate the momentum uncertainty of a tennis ball constrained to be in a fence enclosure of length 35 m surrounding the court in kg m/s.
Is the correct answer "3e-36"? (truth yes, model no)
- h238: A chemical reaction takes place in a container of cross-sectional area $50 \mathrm{~cm}^2$. As a result of the reaction, a piston is pushed out through $15 \mathrm{~cm}$ against an external pressure of $1.0 \mathrm{~atm}$. Calculate the work done by the system.
Is the correct answer "-75 $\mathrm{~J}$"? (truth yes, model no)
- h249: Until what month and year did Gerald Ford serve as the Honorary Grand Master of the International Supreme Council, Order of DeMolay? Is the answer "January 1977"? (truth yes, model no)
- h253: A particle of mass $1.0 \mathrm{~g}$ is released near the surface of the Earth, where the acceleration of free fall is $g=8.91 \mathrm{~m} \mathrm{~s}^{-2}$. What will be its kinetic energy after  $1.0 \mathrm{~s}$. Ignore air resistance?
Is the correct answer "48 $\mathrm{~mJ}$"? (truth yes, model no)
- h262: A math book and a physics book sitting on a table are tied together with a length of string. With the string taut one book is pushed off the edge of the table. As it falls the other book is dragged horizontally across the table surface. With no friction acceleration of the books is
Is the correct answer "dependent on the weight of the books"? (truth no, model yes)
- h264: An airplane is flying at Mach 1.75 at an altitude of 8000 m, where the speed of sound is How long after the plane passes directly overhead will you hear the sonic boom? (Unit: m/s)
Is the correct answer "560"? (truth yes, model no)
- h277: Carbon dioxide is reduced by hydrogen according to the equation CO_2(g) + H_2(g) \rightleftarrows CO(g) + H_2O(g) . One mole of CO_2 is reacted with one mole of H_2 at 825K and it is found that, at equilibrium, 0.27atmof CO is present. Determine the equilibrium constant, K, at 825K .
Is the correct answer "0.137"? (truth yes, model no)
- h279: In the 2012 research paper titled "Multiplication of EEG Samples through Replicating, Biasing, and Overlapping" by Adham Atyabi et al., between what frequencies was the EEG dataset bandpass filtered, in hertz (Hz)? Is the answer "1 & 50"? (truth yes, model no)
- h294: Include air resistance proportional to the square of the ball's speed in the previous problem. Let the drag coefficient be $c_W=0.5$, the softball radius be $5 \mathrm{~cm}$ and the mass be $200 \mathrm{~g}$. Find the initial speed of the softball needed now to clear the fence.
Is the correct answer "32.4$\mathrm{~m} \cdot \mathrm{s}^{-1}$"? (truth no, model yes)
