# Pool run 5: base `claude-haiku-5-5` (effort default, adaptive thinking)

1048 questions processed; 0 hit the 16,000-token cap, gave no FINAL ANSWER or failed claim extraction, and are excluded; base model wrong on **158** of 1048 answered. API cost $8.3268. Contentions are the claims in the visible answer (DEVIATIONS.md, D1–D3).

Test set rule: none (v2 split locked separately in experiments/split-v2.json). Test set: 0 wrong + 0 right. Calibration pool: 0 items.

| id | category | truth | model | correct | set | contentions | related pairs | contradictions |
|---|---|---|---|---|---|---|---|---|
| t001 | puzzle-computed | yes | yes | yes | calib | 8 | 18 | 4 |
| t002 | science-engineering | no | no | yes | calib | 8 | 15 | 3 |
| t003 | science-engineering | yes | yes | yes | calib | 9 | 20 | 3 |
| t004 | science-chemistry | yes | yes | yes | calib | 8 | 19 | 6 |
| t005 | simpleqa | no | no | yes | calib | 8 | 10 | 3 |
| t006 | puzzle-computed | yes | yes | yes | calib | 8 | 20 | 0 |
| t007 | simpleqa | no | no | yes | calib | 7 | 10 | 0 |
| t008 | claim-verified | yes | yes | yes | calib | 8 | 28 | 0 |
| t009 | puzzle-computed | yes | yes | yes | calib | 7 | 9 | 2 |
| t010 | science-physics | yes | yes | yes | calib | 10 | 22 | 4 |
| t011 | puzzle-computed | no | no | yes | calib | 10 | 23 | 0 |
| t012 | puzzle-computed | no | no | yes | calib | 8 | 18 | 0 |
| t013 | science-engineering | no | no | yes | calib | 8 | 20 | 0 |
| t014 | science-physics | no | no | yes | calib | 8 | 20 | 6 |
| t015 | simpleqa | yes | yes | yes | calib | 8 | 11 | 0 |
| t016 | simpleqa | yes | yes | yes | calib | 9 | 21 | 8 |
| t017 | science-engineering | yes | no | **no** | calib | 9 | 27 | 13 |
| t018 | science-chemistry | no | no | yes | calib | 8 | 18 | 0 |
| t019 | science-chemistry | no | no | yes | calib | 9 | 22 | 1 |
| t020 | science-chemistry | no | no | yes | calib | 10 | 17 | 0 |
| t021 | science-physics | yes | yes | yes | calib | 9 | 30 | 7 |
| t022 | puzzle-computed | no | no | yes | calib | 9 | 19 | 0 |
| t023 | puzzle-computed | no | no | yes | calib | 9 | 26 | 10 |
| t024 | puzzle-computed | yes | yes | yes | calib | 8 | 14 | 3 |
| t025 | claim-verified | no | no | yes | calib | 10 | 15 | 1 |
| t026 | claim-verified | no | no | yes | calib | 9 | 26 | 13 |
| t027 | science-biology | yes | yes | yes | calib | 10 | 20 | 5 |
| t028 | simpleqa | yes | yes | yes | calib | 9 | 14 | 3 |
| t029 | science-physics | no | no | yes | calib | 8 | 21 | 0 |
| t030 | science-engineering | no | yes | **no** | calib | 9 | 21 | 1 |
| t031 | science-biology | no | no | yes | calib | 9 | 22 | 7 |
| t032 | claim-verified | no | no | yes | calib | 9 | 15 | 0 |
| t033 | claim-verified | yes | yes | yes | calib | 8 | 21 | 6 |
| t034 | science-engineering | no | no | yes | calib | 10 | 25 | 0 |
| t035 | science-biology | no | no | yes | calib | 8 | 12 | 4 |
| t036 | puzzle-computed | yes | yes | yes | calib | 8 | 22 | 0 |
| t037 | puzzle-computed | no | no | yes | calib | 8 | 19 | 0 |
| t038 | puzzle-computed | yes | yes | yes | calib | 9 | 28 | 7 |
| t039 | science-biology | yes | yes | yes | calib | 9 | 15 | 3 |
| t040 | claim-verified | yes | yes | yes | calib | 8 | 21 | 0 |
| t041 | science-biology | no | no | yes | calib | 8 | 23 | 5 |
| t042 | science-chemistry | yes | yes | yes | calib | 9 | 20 | 2 |
| t043 | simpleqa | no | no | yes | calib | 8 | 19 | 0 |
| t044 | puzzle-computed | yes | yes | yes | calib | 8 | 9 | 0 |
| t045 | simpleqa | no | no | yes | calib | 10 | 22 | 8 |
| t046 | science-physics | yes | no | **no** | calib | 8 | 16 | 3 |
| t047 | simpleqa | no | no | yes | calib | 9 | 18 | 0 |
| t048 | simpleqa | no | yes | **no** | calib | 8 | 18 | 4 |
| t049 | simpleqa | yes | yes | yes | calib | 9 | 18 | 9 |
| t050 | science-engineering | no | no | yes | calib | 10 | 26 | 0 |
| t051 | puzzle-computed | no | no | yes | calib | 9 | 28 | 12 |
| t052 | science-biology | no | no | yes | calib | 10 | 19 | 3 |
| t053 | claim-verified | no | no | yes | calib | 8 | 17 | 0 |
| t054 | simpleqa | no | no | yes | calib | 8 | 16 | 3 |
| t055 | claim-verified | yes | yes | yes | calib | 8 | 28 | 0 |
| t056 | claim-verified | yes | yes | yes | calib | 8 | 22 | 4 |
| t057 | puzzle-computed | yes | yes | yes | calib | 10 | 19 | 3 |
| t058 | puzzle-computed | yes | yes | yes | calib | 8 | 24 | 0 |
| t059 | puzzle-computed | yes | yes | yes | calib | 8 | 14 | 2 |
| t060 | puzzle-computed | yes | yes | yes | calib | 8 | 21 | 3 |
| t061 | puzzle-computed | yes | yes | yes | calib | 8 | 21 | 0 |
| t062 | simpleqa | no | no | yes | calib | 7 | 14 | 3 |
| t063 | puzzle-computed | no | no | yes | calib | 10 | 21 | 6 |
| t064 | science-biology | no | no | yes | calib | 10 | 36 | 15 |
| t065 | science-chemistry | yes | no | **no** | calib | 9 | 12 | 0 |
| t066 | simpleqa | no | no | yes | calib | 9 | 13 | 0 |
| t067 | puzzle-computed | no | no | yes | calib | 9 | 22 | 3 |
| t068 | claim-verified | yes | yes | yes | calib | 9 | 19 | 0 |
| t069 | science-physics | yes | yes | yes | calib | 9 | 22 | 0 |
| t070 | science-biology | no | no | yes | calib | 9 | 26 | 6 |
| t071 | claim-verified | no | no | yes | calib | 10 | 39 | 11 |
| t072 | claim-verified | no | no | yes | calib | 8 | 10 | 0 |
| t073 | puzzle-computed | yes | yes | yes | calib | 8 | 19 | 3 |
| t074 | puzzle-computed | yes | yes | yes | calib | 8 | 16 | 4 |
| t075 | science-physics | yes | yes | yes | calib | 9 | 17 | 3 |
| t076 | science-physics | yes | yes | yes | calib | 9 | 28 | 0 |
| t077 | science-chemistry | no | no | yes | calib | 9 | 22 | 0 |
| t078 | simpleqa | yes | no | **no** | calib | 9 | 18 | 5 |
| t079 | science-engineering | yes | yes | yes | calib | 9 | 17 | 4 |
| t080 | puzzle-computed | yes | yes | yes | calib | 9 | 15 | 0 |
| t081 | puzzle-computed | no | no | yes | calib | 8 | 15 | 0 |
| t082 | simpleqa | yes | no | **no** | calib | 9 | 15 | 2 |
| t083 | simpleqa | yes | yes | yes | calib | 9 | 27 | 6 |
| t084 | simpleqa | yes | no | **no** | calib | 10 | 15 | 4 |
| t085 | puzzle-computed | no | no | yes | calib | 9 | 32 | 10 |
| t086 | science-chemistry | yes | yes | yes | calib | 8 | 17 | 2 |
| t087 | puzzle-computed | no | no | yes | calib | 10 | 22 | 0 |
| t088 | claim-verified | no | no | yes | calib | 10 | 18 | 0 |
| t089 | science-engineering | yes | yes | yes | calib | 10 | 26 | 5 |
| t090 | science-engineering | no | no | yes | calib | 8 | 17 | 1 |
| t091 | simpleqa | no | no | yes | calib | 7 | 10 | 0 |
| t092 | simpleqa | no | no | yes | calib | 6 | 10 | 4 |
| t093 | science-chemistry | no | no | yes | calib | 9 | 26 | 0 |
| t094 | claim-verified | no | no | yes | calib | 7 | 12 | 0 |
| t095 | puzzle-computed | yes | yes | yes | calib | 10 | 40 | 0 |
| t096 | simpleqa | yes | yes | yes | calib | 10 | 31 | 15 |
| t097 | simpleqa | yes | yes | yes | calib | 8 | 21 | 0 |
| t098 | simpleqa | yes | yes | yes | calib | 10 | 23 | 7 |
| t099 | science-biology | yes | yes | yes | calib | 9 | 27 | 7 |
| t100 | science-biology | yes | yes | yes | calib | 9 | 18 | 2 |
| t1000 | simpleqa | yes | no | **no** | calib | 9 | 19 | 9 |
| t1001 | science-chemistry | no | no | yes | calib | 9 | 26 | 6 |
| t1002 | science-chemistry | yes | yes | yes | calib | 8 | 24 | 6 |
| t1003 | science-physics | no | no | yes | calib | 10 | 37 | 0 |
| t1004 | simpleqa | no | no | yes | calib | 10 | 25 | 10 |
| t1005 | science-physics | no | no | yes | calib | 8 | 22 | 4 |
| t1006 | simpleqa | yes | yes | yes | calib | 7 | 17 | 8 |
| t1007 | science-engineering | no | no | yes | calib | 9 | 23 | 0 |
| t1008 | simpleqa | yes | yes | yes | calib | 9 | 24 | 10 |
| t1009 | simpleqa | yes | yes | yes | calib | 10 | 20 | 3 |
| t101 | science-biology | no | no | yes | calib | 8 | 20 | 3 |
| t1010 | science-chemistry | yes | yes | yes | calib | 8 | 15 | 4 |
| t1011 | science-chemistry | no | no | yes | calib | 9 | 26 | 0 |
| t1012 | science-chemistry | no | yes | **no** | calib | 10 | 24 | 0 |
| t1013 | science-engineering | yes | no | **no** | calib | 8 | 14 | 3 |
| t1014 | science-physics | no | no | yes | calib | 7 | 19 | 0 |
| t1015 | simpleqa | no | no | yes | calib | 8 | 23 | 0 |
| t1016 | science-physics | yes | yes | yes | calib | 9 | 25 | 0 |
| t1017 | science-physics | no | no | yes | calib | 8 | 15 | 0 |
| t1018 | simpleqa | no | no | yes | calib | 9 | 13 | 3 |
| t1019 | simpleqa | no | no | yes | calib | 7 | 17 | 0 |
| t102 | claim-verified | yes | yes | yes | calib | 7 | 19 | 6 |
| t1020 | science-chemistry | no | no | yes | calib | 7 | 17 | 0 |
| t1021 | science-physics | yes | yes | yes | calib | 10 | 29 | 7 |
| t1022 | science-engineering | no | no | yes | calib | 10 | 24 | 9 |
| t1023 | science-chemistry | no | no | yes | calib | 9 | 24 | 0 |
| t1024 | science-chemistry | no | no | yes | calib | 9 | 15 | 0 |
| t1025 | science-chemistry | yes | yes | yes | calib | 9 | 36 | 1 |
| t1026 | science-physics | yes | yes | yes | calib | 9 | 15 | 4 |
| t1027 | simpleqa | yes | yes | yes | calib | 9 | 20 | 6 |
| t1028 | science-engineering | yes | no | **no** | calib | 8 | 16 | 3 |
| t1029 | science-physics | no | no | yes | calib | 9 | 23 | 4 |
| t103 | simpleqa | yes | yes | yes | calib | 9 | 12 | 2 |
| t1030 | science-engineering | no | no | yes | calib | 11 | 17 | 6 |
| t1031 | simpleqa | no | no | yes | calib | 10 | 15 | 4 |
| t1032 | simpleqa | yes | no | **no** | calib | 8 | 17 | 1 |
| t1033 | science-chemistry | no | no | yes | calib | 8 | 27 | 0 |
| t1034 | science-engineering | yes | yes | yes | calib | 9 | 20 | 5 |
| t1035 | science-chemistry | yes | yes | yes | calib | 9 | 19 | 5 |
| t1036 | science-physics | yes | yes | yes | calib | 9 | 27 | 10 |
| t1037 | science-engineering | no | no | yes | calib | 8 | 13 | 1 |
| t1038 | science-physics | no | no | yes | calib | 8 | 15 | 1 |
| t1039 | science-engineering | no | no | yes | calib | 9 | 22 | 4 |
| t104 | puzzle-computed | yes | yes | yes | calib | 9 | 22 | 0 |
| t1040 | simpleqa | no | no | yes | calib | 8 | 16 | 0 |
| t1041 | science-physics | no | no | yes | calib | 9 | 20 | 0 |
| t1042 | simpleqa | yes | yes | yes | calib | 8 | 12 | 3 |
| t1043 | science-chemistry | yes | yes | yes | calib | 9 | 19 | 2 |
| t1044 | simpleqa | no | yes | **no** | calib | 10 | 29 | 12 |
| t1045 | science-physics | yes | yes | yes | calib | 8 | 16 | 6 |
| t1046 | simpleqa | yes | yes | yes | calib | 10 | 25 | 6 |
| t1047 | simpleqa | yes | no | **no** | calib | 7 | 11 | 1 |
| t1048 | simpleqa | yes | yes | yes | calib | 9 | 12 | 5 |
| t105 | simpleqa | no | yes | **no** | calib | 8 | 15 | 4 |
| t106 | puzzle-computed | yes | yes | yes | calib | 9 | 23 | 0 |
| t107 | puzzle-computed | no | no | yes | calib | 9 | 21 | 0 |
| t108 | simpleqa | no | no | yes | calib | 8 | 22 | 10 |
| t109 | puzzle-computed | yes | yes | yes | calib | 8 | 21 | 6 |
| t110 | science-physics | yes | yes | yes | calib | 8 | 18 | 8 |
| t111 | claim-verified | yes | yes | yes | calib | 9 | 20 | 3 |
| t112 | science-chemistry | yes | yes | yes | calib | 9 | 20 | 1 |
| t113 | puzzle-computed | yes | yes | yes | calib | 10 | 23 | 0 |
| t114 | simpleqa | yes | yes | yes | calib | 8 | 22 | 13 |
| t115 | simpleqa | no | no | yes | calib | 9 | 27 | 0 |
| t116 | simpleqa | yes | yes | yes | calib | 8 | 24 | 6 |
| t117 | claim-verified | yes | yes | yes | calib | 9 | 36 | 0 |
| t118 | puzzle-computed | yes | yes | yes | calib | 8 | 17 | 0 |
| t119 | simpleqa | no | no | yes | calib | 9 | 21 | 7 |
| t120 | claim-verified | yes | yes | yes | calib | 9 | 24 | 4 |
| t121 | simpleqa | yes | yes | yes | calib | 11 | 28 | 10 |
| t122 | puzzle-computed | yes | yes | yes | calib | 8 | 19 | 0 |
| t123 | puzzle-computed | no | no | yes | calib | 8 | 16 | 1 |
| t124 | simpleqa | yes | no | **no** | calib | 8 | 18 | 0 |
| t125 | science-physics | no | no | yes | calib | 8 | 19 | 0 |
| t126 | puzzle-computed | no | no | yes | calib | 8 | 26 | 7 |
| t127 | simpleqa | no | no | yes | calib | 10 | 34 | 8 |
| t128 | science-biology | no | no | yes | calib | 8 | 17 | 4 |
| t129 | simpleqa | yes | yes | yes | calib | 10 | 30 | 5 |
| t130 | puzzle-computed | no | no | yes | calib | 9 | 32 | 10 |
| t131 | science-engineering | yes | yes | yes | calib | 8 | 21 | 6 |
| t132 | puzzle-computed | yes | yes | yes | calib | 11 | 26 | 0 |
| t133 | science-chemistry | no | no | yes | calib | 6 | 12 | 3 |
| t134 | simpleqa | yes | yes | yes | calib | 8 | 14 | 3 |
| t135 | simpleqa | no | no | yes | calib | 8 | 6 | 0 |
| t136 | science-engineering | no | no | yes | calib | 9 | 25 | 11 |
| t137 | claim-verified | yes | yes | yes | calib | 8 | 12 | 1 |
| t138 | simpleqa | no | no | yes | calib | 9 | 25 | 6 |
| t139 | puzzle-computed | yes | yes | yes | calib | 8 | 15 | 1 |
| t140 | science-chemistry | no | no | yes | calib | 8 | 18 | 5 |
| t141 | simpleqa | yes | yes | yes | calib | 9 | 23 | 7 |
| t142 | science-chemistry | no | no | yes | calib | 9 | 24 | 3 |
| t143 | simpleqa | no | no | yes | calib | 8 | 15 | 0 |
| t144 | puzzle-computed | yes | yes | yes | calib | 8 | 22 | 4 |
| t145 | science-biology | no | no | yes | calib | 8 | 23 | 9 |
| t146 | science-biology | yes | yes | yes | calib | 9 | 18 | 2 |
| t147 | puzzle-computed | yes | yes | yes | calib | 8 | 20 | 0 |
| t148 | science-engineering | no | no | yes | calib | 8 | 21 | 0 |
| t149 | puzzle-computed | no | no | yes | calib | 8 | 15 | 2 |
| t150 | puzzle-computed | yes | yes | yes | calib | 9 | 18 | 0 |
| t151 | puzzle-computed | yes | yes | yes | calib | 9 | 25 | 3 |
| t152 | claim-verified | yes | yes | yes | calib | 9 | 12 | 0 |
| t153 | science-physics | no | no | yes | calib | 8 | 21 | 7 |
| t154 | simpleqa | no | no | yes | calib | 8 | 22 | 0 |
| t155 | claim-verified | no | no | yes | calib | 8 | 19 | 0 |
| t156 | simpleqa | yes | no | **no** | calib | 8 | 12 | 5 |
| t157 | science-physics | yes | yes | yes | calib | 9 | 27 | 4 |
| t158 | science-biology | yes | yes | yes | calib | 10 | 22 | 6 |
| t159 | puzzle-computed | no | no | yes | calib | 9 | 26 | 6 |
| t160 | simpleqa | yes | no | **no** | calib | 9 | 13 | 2 |
| t161 | simpleqa | no | no | yes | calib | 8 | 18 | 0 |
| t162 | science-engineering | no | no | yes | calib | 9 | 27 | 0 |
| t163 | puzzle-computed | yes | yes | yes | calib | 9 | 31 | 7 |
| t164 | science-physics | yes | no | **no** | calib | 11 | 24 | 6 |
| t165 | puzzle-computed | no | no | yes | calib | 8 | 17 | 4 |
| t166 | claim-verified | yes | yes | yes | calib | 8 | 14 | 1 |
| t167 | simpleqa | yes | no | **no** | calib | 9 | 20 | 5 |
| t168 | claim-verified | no | no | yes | calib | 8 | 17 | 1 |
| t169 | simpleqa | no | yes | **no** | calib | 8 | 11 | 3 |
| t170 | puzzle-computed | yes | yes | yes | calib | 9 | 28 | 0 |
| t171 | simpleqa | no | yes | **no** | calib | 8 | 16 | 8 |
| t172 | puzzle-computed | no | no | yes | calib | 8 | 21 | 5 |
| t173 | claim-verified | yes | yes | yes | calib | 9 | 22 | 0 |
| t174 | science-physics | no | no | yes | calib | 10 | 31 | 0 |
| t175 | science-biology | no | no | yes | calib | 9 | 11 | 0 |
| t176 | science-chemistry | yes | yes | yes | calib | 7 | 15 | 0 |
| t177 | claim-verified | yes | yes | yes | calib | 8 | 13 | 0 |
| t178 | puzzle-computed | yes | yes | yes | calib | 8 | 14 | 1 |
| t179 | simpleqa | yes | yes | yes | calib | 9 | 19 | 5 |
| t180 | simpleqa | no | no | yes | calib | 8 | 20 | 5 |
| t181 | science-chemistry | no | no | yes | calib | 8 | 15 | 1 |
| t182 | puzzle-computed | no | no | yes | calib | 9 | 33 | 0 |
| t183 | science-chemistry | yes | yes | yes | calib | 10 | 27 | 5 |
| t184 | simpleqa | no | no | yes | calib | 8 | 14 | 0 |
| t185 | claim-verified | yes | yes | yes | calib | 8 | 23 | 0 |
| t186 | science-biology | yes | yes | yes | calib | 9 | 22 | 5 |
| t187 | simpleqa | no | no | yes | calib | 8 | 19 | 0 |
| t188 | puzzle-computed | yes | yes | yes | calib | 11 | 55 | 0 |
| t189 | claim-verified | no | no | yes | calib | 9 | 17 | 0 |
| t190 | puzzle-computed | yes | yes | yes | calib | 8 | 21 | 4 |
| t191 | simpleqa | no | no | yes | calib | 6 | 8 | 0 |
| t192 | science-physics | yes | yes | yes | calib | 8 | 25 | 4 |
| t193 | puzzle-computed | yes | yes | yes | calib | 8 | 22 | 5 |
| t194 | claim-verified | no | no | yes | calib | 7 | 16 | 3 |
| t195 | simpleqa | no | no | yes | calib | 8 | 16 | 6 |
| t196 | simpleqa | yes | yes | yes | calib | 8 | 15 | 4 |
| t197 | puzzle-computed | yes | yes | yes | calib | 8 | 6 | 0 |
| t198 | simpleqa | yes | no | **no** | calib | 8 | 17 | 2 |
| t199 | claim-verified | no | no | yes | calib | 9 | 20 | 5 |
| t200 | simpleqa | yes | yes | yes | calib | 9 | 23 | 6 |
| t201 | claim-verified | yes | yes | yes | calib | 9 | 25 | 1 |
| t202 | science-engineering | yes | yes | yes | calib | 10 | 32 | 0 |
| t203 | science-engineering | no | no | yes | calib | 8 | 19 | 0 |
| t204 | simpleqa | no | no | yes | calib | 8 | 11 | 0 |
| t205 | science-chemistry | no | no | yes | calib | 8 | 18 | 0 |
| t206 | puzzle-computed | yes | yes | yes | calib | 7 | 21 | 0 |
| t207 | puzzle-computed | no | no | yes | calib | 9 | 23 | 7 |
| t208 | puzzle-computed | yes | yes | yes | calib | 10 | 32 | 5 |
| t209 | simpleqa | no | no | yes | calib | 9 | 20 | 7 |
| t210 | puzzle-computed | yes | yes | yes | calib | 10 | 16 | 0 |
| t211 | science-biology | yes | yes | yes | calib | 9 | 21 | 9 |
| t212 | puzzle-computed | no | no | yes | calib | 9 | 24 | 0 |
| t213 | science-biology | yes | yes | yes | calib | 9 | 36 | 20 |
| t214 | simpleqa | no | no | yes | calib | 9 | 28 | 0 |
| t215 | claim-verified | yes | yes | yes | calib | 8 | 23 | 4 |
| t216 | simpleqa | no | no | yes | calib | 9 | 20 | 6 |
| t217 | science-physics | no | no | yes | calib | 7 | 18 | 4 |
| t218 | puzzle-computed | no | no | yes | calib | 8 | 17 | 3 |
| t219 | science-biology | no | no | yes | calib | 10 | 18 | 1 |
| t220 | science-physics | no | no | yes | calib | 10 | 21 | 10 |
| t221 | puzzle-computed | yes | yes | yes | calib | 9 | 32 | 4 |
| t222 | claim-verified | no | no | yes | calib | 9 | 32 | 7 |
| t223 | science-physics | yes | yes | yes | calib | 8 | 23 | 4 |
| t224 | puzzle-computed | yes | yes | yes | calib | 10 | 41 | 5 |
| t225 | claim-verified | yes | yes | yes | calib | 8 | 23 | 0 |
| t226 | science-physics | yes | yes | yes | calib | 6 | 15 | 0 |
| t227 | puzzle-computed | yes | yes | yes | calib | 9 | 22 | 2 |
| t228 | claim-verified | yes | yes | yes | calib | 7 | 13 | 0 |
| t229 | science-biology | yes | yes | yes | calib | 9 | 18 | 1 |
| t230 | science-physics | no | no | yes | calib | 7 | 19 | 6 |
| t231 | science-engineering | yes | yes | yes | calib | 8 | 23 | 7 |
| t232 | claim-verified | yes | yes | yes | calib | 8 | 28 | 0 |
| t233 | claim-verified | no | no | yes | calib | 9 | 26 | 5 |
| t234 | science-biology | no | no | yes | calib | 8 | 23 | 2 |
| t235 | simpleqa | no | no | yes | calib | 8 | 12 | 0 |
| t236 | puzzle-computed | no | no | yes | calib | 8 | 16 | 0 |
| t237 | science-chemistry | yes | yes | yes | calib | 8 | 19 | 4 |
| t238 | science-engineering | yes | yes | yes | calib | 10 | 23 | 8 |
| t239 | simpleqa | yes | no | **no** | calib | 9 | 15 | 4 |
| t240 | puzzle-computed | no | no | yes | calib | 10 | 28 | 0 |
| t241 | claim-verified | yes | yes | yes | calib | 6 | 14 | 0 |
| t242 | science-chemistry | no | no | yes | calib | 8 | 17 | 3 |
| t243 | puzzle-computed | no | no | yes | calib | 8 | 28 | 0 |
| t244 | puzzle-computed | no | no | yes | calib | 10 | 28 | 7 |
| t245 | simpleqa | no | no | yes | calib | 10 | 19 | 5 |
| t246 | simpleqa | no | no | yes | calib | 8 | 11 | 5 |
| t247 | puzzle-computed | yes | yes | yes | calib | 10 | 32 | 0 |
| t248 | simpleqa | no | no | yes | calib | 8 | 22 | 5 |
| t249 | puzzle-computed | no | no | yes | calib | 9 | 33 | 7 |
| t250 | simpleqa | no | yes | **no** | calib | 10 | 26 | 9 |
| t251 | science-chemistry | no | yes | **no** | calib | 10 | 25 | 4 |
| t252 | simpleqa | no | no | yes | calib | 8 | 25 | 0 |
| t253 | simpleqa | no | no | yes | calib | 9 | 28 | 7 |
| t254 | puzzle-computed | no | no | yes | calib | 10 | 37 | 2 |
| t255 | simpleqa | no | no | yes | calib | 6 | 14 | 4 |
| t256 | puzzle-computed | yes | yes | yes | calib | 9 | 23 | 2 |
| t257 | science-physics | no | no | yes | calib | 9 | 36 | 0 |
| t258 | simpleqa | yes | yes | yes | calib | 10 | 23 | 6 |
| t259 | puzzle-computed | yes | yes | yes | calib | 8 | 21 | 0 |
| t260 | puzzle-computed | no | no | yes | calib | 9 | 21 | 0 |
| t261 | simpleqa | no | no | yes | calib | 9 | 28 | 0 |
| t262 | science-physics | yes | yes | yes | calib | 9 | 30 | 0 |
| t263 | science-chemistry | no | no | yes | calib | 9 | 31 | 7 |
| t264 | simpleqa | no | no | yes | calib | 8 | 19 | 0 |
| t265 | claim-verified | yes | yes | yes | calib | 8 | 27 | 0 |
| t266 | puzzle-computed | no | no | yes | calib | 9 | 25 | 0 |
| t267 | science-physics | yes | no | **no** | calib | 10 | 29 | 4 |
| t268 | science-biology | yes | yes | yes | calib | 10 | 26 | 1 |
| t269 | science-engineering | yes | no | **no** | calib | 11 | 24 | 4 |
| t270 | simpleqa | no | no | yes | calib | 7 | 16 | 6 |
| t271 | puzzle-computed | yes | yes | yes | calib | 9 | 25 | 0 |
| t272 | science-engineering | yes | yes | yes | calib | 9 | 22 | 5 |
| t273 | claim-verified | yes | yes | yes | calib | 8 | 15 | 0 |
| t274 | science-engineering | yes | no | **no** | calib | 9 | 9 | 1 |
| t275 | science-chemistry | yes | yes | yes | calib | 9 | 18 | 7 |
| t276 | science-physics | no | no | yes | calib | 8 | 21 | 0 |
| t277 | claim-verified | no | no | yes | calib | 9 | 27 | 0 |
| t278 | simpleqa | no | no | yes | calib | 6 | 10 | 4 |
| t279 | simpleqa | yes | no | **no** | calib | 9 | 22 | 5 |
| t280 | claim-verified | yes | yes | yes | calib | 8 | 21 | 5 |
| t281 | science-chemistry | no | no | yes | calib | 9 | 24 | 4 |
| t282 | science-engineering | no | no | yes | calib | 8 | 26 | 7 |
| t283 | puzzle-computed | yes | yes | yes | calib | 9 | 16 | 1 |
| t284 | simpleqa | no | no | yes | calib | 9 | 25 | 7 |
| t285 | claim-verified | no | no | yes | calib | 9 | 18 | 0 |
| t286 | claim-verified | no | no | yes | calib | 7 | 6 | 0 |
| t287 | science-biology | no | no | yes | calib | 9 | 26 | 11 |
| t288 | science-engineering | yes | yes | yes | calib | 10 | 16 | 0 |
| t289 | science-physics | no | no | yes | calib | 7 | 21 | 0 |
| t290 | claim-verified | yes | yes | yes | calib | 7 | 18 | 2 |
| t291 | puzzle-computed | no | no | yes | calib | 9 | 27 | 0 |
| t292 | claim-verified | yes | yes | yes | calib | 9 | 36 | 0 |
| t293 | science-chemistry | yes | yes | yes | calib | 7 | 16 | 0 |
| t294 | science-biology | yes | no | **no** | calib | 11 | 29 | 1 |
| t295 | science-engineering | yes | yes | yes | calib | 10 | 23 | 0 |
| t296 | simpleqa | yes | yes | yes | calib | 8 | 11 | 4 |
| t297 | simpleqa | no | no | yes | calib | 9 | 16 | 6 |
| t298 | claim-verified | no | no | yes | calib | 7 | 12 | 0 |
| t299 | simpleqa | no | no | yes | calib | 9 | 22 | 0 |
| t300 | puzzle-computed | no | no | yes | calib | 10 | 44 | 0 |
| t301 | science-physics | no | no | yes | calib | 8 | 15 | 0 |
| t302 | science-physics | no | yes | **no** | calib | 10 | 26 | 0 |
| t303 | science-chemistry | yes | no | **no** | calib | 10 | 23 | 3 |
| t304 | simpleqa | yes | yes | yes | calib | 9 | 25 | 8 |
| t305 | science-physics | yes | yes | yes | calib | 9 | 17 | 3 |
| t306 | claim-verified | no | no | yes | calib | 8 | 22 | 0 |
| t307 | puzzle-computed | no | no | yes | calib | 7 | 14 | 0 |
| t308 | simpleqa | no | no | yes | calib | 8 | 15 | 4 |
| t309 | claim-verified | yes | yes | yes | calib | 8 | 28 | 0 |
| t310 | puzzle-computed | no | no | yes | calib | 8 | 14 | 2 |
| t311 | science-physics | yes | yes | yes | calib | 8 | 21 | 0 |
| t312 | simpleqa | yes | no | **no** | calib | 7 | 13 | 4 |
| t313 | simpleqa | no | no | yes | calib | 7 | 12 | 2 |
| t314 | puzzle-computed | yes | yes | yes | calib | 8 | 21 | 5 |
| t315 | science-engineering | yes | no | **no** | calib | 9 | 24 | 4 |
| t316 | puzzle-computed | yes | yes | yes | calib | 8 | 27 | 0 |
| t317 | simpleqa | yes | no | **no** | calib | 8 | 13 | 6 |
| t318 | simpleqa | no | no | yes | calib | 9 | 24 | 4 |
| t319 | claim-verified | no | no | yes | calib | 9 | 17 | 6 |
| t320 | simpleqa | yes | no | **no** | calib | 9 | 22 | 6 |
| t321 | science-physics | no | no | yes | calib | 8 | 13 | 0 |
| t322 | science-biology | yes | yes | yes | calib | 9 | 25 | 3 |
| t323 | simpleqa | yes | no | **no** | calib | 9 | 25 | 6 |
| t324 | simpleqa | no | no | yes | calib | 9 | 28 | 8 |
| t325 | simpleqa | no | no | yes | calib | 8 | 16 | 0 |
| t326 | science-physics | no | no | yes | calib | 8 | 22 | 7 |
| t327 | science-biology | yes | yes | yes | calib | 9 | 15 | 4 |
| t328 | science-biology | no | no | yes | calib | 10 | 19 | 1 |
| t329 | simpleqa | no | no | yes | calib | 8 | 17 | 0 |
| t330 | simpleqa | no | no | yes | calib | 7 | 11 | 3 |
| t331 | puzzle-computed | yes | yes | yes | calib | 9 | 27 | 6 |
| t332 | puzzle-computed | no | no | yes | calib | 8 | 18 | 3 |
| t333 | claim-verified | yes | yes | yes | calib | 7 | 15 | 1 |
| t334 | claim-verified | no | no | yes | calib | 9 | 36 | 8 |
| t335 | science-physics | no | no | yes | calib | 8 | 28 | 0 |
| t336 | claim-verified | yes | yes | yes | calib | 8 | 19 | 1 |
| t337 | simpleqa | no | no | yes | calib | 8 | 22 | 11 |
| t338 | simpleqa | yes | yes | yes | calib | 8 | 14 | 4 |
| t339 | science-engineering | yes | no | **no** | calib | 10 | 19 | 4 |
| t340 | simpleqa | no | no | yes | calib | 10 | 17 | 5 |
| t341 | science-physics | no | no | yes | calib | 7 | 11 | 0 |
| t342 | claim-verified | no | no | yes | calib | 8 | 21 | 0 |
| t343 | claim-verified | no | no | yes | calib | 9 | 20 | 14 |
| t344 | puzzle-computed | no | no | yes | calib | 8 | 17 | 1 |
| t345 | simpleqa | yes | no | **no** | calib | 9 | 20 | 6 |
| t346 | simpleqa | yes | no | **no** | calib | 9 | 21 | 4 |
| t347 | claim-verified | yes | yes | yes | calib | 7 | 17 | 3 |
| t348 | puzzle-computed | no | no | yes | calib | 9 | 20 | 6 |
| t349 | science-chemistry | no | no | yes | calib | 10 | 20 | 1 |
| t350 | simpleqa | yes | no | **no** | calib | 9 | 23 | 7 |
| t351 | puzzle-computed | no | no | yes | calib | 9 | 15 | 0 |
| t352 | science-chemistry | yes | yes | yes | calib | 8 | 17 | 4 |
| t353 | claim-verified | no | no | yes | calib | 8 | 13 | 4 |
| t354 | claim-verified | no | no | yes | calib | 8 | 13 | 0 |
| t355 | simpleqa | yes | yes | yes | calib | 9 | 22 | 7 |
| t356 | puzzle-computed | yes | yes | yes | calib | 8 | 16 | 4 |
| t357 | simpleqa | yes | no | **no** | calib | 9 | 25 | 7 |
| t358 | science-physics | no | no | yes | calib | 8 | 19 | 0 |
| t359 | simpleqa | yes | yes | yes | calib | 8 | 18 | 5 |
| t360 | simpleqa | yes | no | **no** | calib | 9 | 25 | 7 |
| t361 | puzzle-computed | no | no | yes | calib | 10 | 32 | 11 |
| t362 | simpleqa | yes | no | **no** | calib | 9 | 23 | 9 |
| t363 | simpleqa | yes | no | **no** | calib | 8 | 15 | 6 |
| t364 | puzzle-computed | yes | yes | yes | calib | 10 | 16 | 1 |
| t365 | puzzle-computed | no | no | yes | calib | 8 | 26 | 7 |
| t366 | science-biology | yes | yes | yes | calib | 9 | 17 | 3 |
| t367 | puzzle-computed | yes | yes | yes | calib | 8 | 14 | 1 |
| t368 | simpleqa | yes | no | **no** | calib | 10 | 25 | 3 |
| t369 | claim-verified | no | no | yes | calib | 8 | 17 | 1 |
| t370 | science-engineering | no | no | yes | calib | 8 | 15 | 5 |
| t371 | puzzle-computed | no | no | yes | calib | 8 | 11 | 0 |
| t372 | puzzle-computed | yes | yes | yes | calib | 7 | 17 | 0 |
| t373 | science-chemistry | no | no | yes | calib | 9 | 22 | 1 |
| t374 | science-engineering | no | no | yes | calib | 9 | 19 | 0 |
| t375 | science-biology | yes | yes | yes | calib | 9 | 21 | 0 |
| t376 | puzzle-computed | no | no | yes | calib | 8 | 16 | 4 |
| t377 | claim-verified | yes | yes | yes | calib | 8 | 22 | 2 |
| t378 | science-biology | no | no | yes | calib | 8 | 19 | 0 |
| t379 | puzzle-computed | yes | yes | yes | calib | 8 | 15 | 3 |
| t380 | puzzle-computed | yes | yes | yes | calib | 9 | 17 | 1 |
| t381 | simpleqa | yes | no | **no** | calib | 8 | 22 | 4 |
| t382 | claim-verified | yes | yes | yes | calib | 7 | 15 | 0 |
| t383 | simpleqa | yes | yes | yes | calib | 9 | 15 | 5 |
| t384 | puzzle-computed | yes | yes | yes | calib | 10 | 33 | 0 |
| t385 | puzzle-computed | yes | yes | yes | calib | 9 | 18 | 4 |
| t386 | puzzle-computed | no | no | yes | calib | 9 | 25 | 0 |
| t387 | science-engineering | no | no | yes | calib | 10 | 19 | 4 |
| t388 | claim-verified | yes | yes | yes | calib | 8 | 28 | 0 |
| t389 | science-engineering | yes | no | **no** | calib | 10 | 20 | 4 |
| t390 | puzzle-computed | no | no | yes | calib | 9 | 33 | 4 |
| t391 | science-biology | no | no | yes | calib | 10 | 28 | 5 |
| t392 | claim-verified | no | no | yes | calib | 8 | 21 | 6 |
| t393 | claim-verified | no | no | yes | calib | 9 | 22 | 0 |
| t394 | science-physics | yes | yes | yes | calib | 8 | 17 | 6 |
| t395 | science-physics | yes | yes | yes | calib | 7 | 15 | 5 |
| t396 | simpleqa | no | no | yes | calib | 9 | 19 | 1 |
| t397 | simpleqa | yes | no | **no** | calib | 9 | 21 | 4 |
| t398 | science-physics | no | no | yes | calib | 8 | 15 | 0 |
| t399 | science-engineering | no | no | yes | calib | 9 | 28 | 5 |
| t400 | puzzle-computed | yes | yes | yes | calib | 8 | 20 | 0 |
| t401 | claim-verified | no | no | yes | calib | 10 | 18 | 0 |
| t402 | claim-verified | yes | yes | yes | calib | 8 | 28 | 0 |
| t403 | puzzle-computed | yes | yes | yes | calib | 9 | 25 | 2 |
| t404 | science-biology | no | no | yes | calib | 10 | 19 | 0 |
| t405 | puzzle-computed | yes | yes | yes | calib | 9 | 15 | 1 |
| t406 | science-biology | no | no | yes | calib | 9 | 17 | 0 |
| t407 | claim-verified | yes | yes | yes | calib | 9 | 13 | 4 |
| t408 | science-chemistry | yes | yes | yes | calib | 8 | 27 | 0 |
| t409 | science-physics | no | no | yes | calib | 8 | 23 | 0 |
| t410 | simpleqa | yes | yes | yes | calib | 10 | 27 | 5 |
| t411 | science-biology | no | no | yes | calib | 8 | 21 | 7 |
| t412 | simpleqa | yes | yes | yes | calib | 10 | 22 | 3 |
| t413 | puzzle-computed | no | no | yes | calib | 9 | 23 | 0 |
| t414 | puzzle-computed | yes | yes | yes | calib | 9 | 34 | 6 |
| t415 | science-engineering | no | no | yes | calib | 8 | 19 | 7 |
| t416 | simpleqa | yes | yes | yes | calib | 8 | 21 | 7 |
| t417 | science-biology | yes | yes | yes | calib | 9 | 11 | 2 |
| t418 | science-chemistry | yes | yes | yes | calib | 8 | 17 | 0 |
| t419 | science-chemistry | no | no | yes | calib | 9 | 27 | 0 |
| t420 | puzzle-computed | no | no | yes | calib | 8 | 20 | 0 |
| t421 | science-chemistry | yes | no | **no** | calib | 8 | 17 | 4 |
| t422 | science-biology | no | no | yes | calib | 9 | 36 | 10 |
| t423 | science-biology | yes | yes | yes | calib | 9 | 14 | 5 |
| t424 | science-physics | no | no | yes | calib | 7 | 17 | 0 |
| t425 | science-biology | no | no | yes | calib | 10 | 12 | 3 |
| t426 | claim-verified | yes | yes | yes | calib | 7 | 15 | 0 |
| t427 | science-biology | no | no | yes | calib | 10 | 20 | 1 |
| t428 | science-chemistry | yes | yes | yes | calib | 9 | 21 | 3 |
| t429 | claim-verified | yes | yes | yes | calib | 8 | 21 | 0 |
| t430 | puzzle-computed | no | no | yes | calib | 8 | 16 | 0 |
| t431 | puzzle-computed | no | no | yes | calib | 8 | 23 | 4 |
| t432 | science-chemistry | yes | no | **no** | calib | 8 | 16 | 3 |
| t433 | puzzle-computed | yes | yes | yes | calib | 8 | 16 | 0 |
| t434 | simpleqa | yes | no | **no** | calib | 10 | 19 | 3 |
| t435 | puzzle-computed | no | no | yes | calib | 10 | 28 | 1 |
| t436 | puzzle-computed | yes | yes | yes | calib | 9 | 19 | 5 |
| t437 | simpleqa | yes | no | **no** | calib | 8 | 13 | 4 |
| t438 | puzzle-computed | yes | yes | yes | calib | 9 | 22 | 4 |
| t439 | simpleqa | yes | no | **no** | calib | 8 | 14 | 0 |
| t440 | science-chemistry | no | no | yes | calib | 9 | 24 | 4 |
| t441 | claim-verified | no | no | yes | calib | 9 | 33 | 0 |
| t442 | puzzle-computed | no | no | yes | calib | 8 | 28 | 0 |
| t443 | simpleqa | yes | yes | yes | calib | 8 | 26 | 12 |
| t444 | science-biology | yes | no | **no** | calib | 9 | 32 | 9 |
| t445 | science-engineering | no | no | yes | calib | 9 | 25 | 0 |
| t446 | simpleqa | no | no | yes | calib | 8 | 14 | 1 |
| t447 | science-engineering | yes | yes | yes | calib | 8 | 23 | 0 |
| t448 | simpleqa | yes | yes | yes | calib | 8 | 23 | 11 |
| t449 | puzzle-computed | no | no | yes | calib | 8 | 23 | 8 |
| t450 | puzzle-computed | yes | yes | yes | calib | 8 | 17 | 1 |
| t451 | puzzle-computed | no | no | yes | calib | 9 | 16 | 0 |
| t452 | claim-verified | yes | yes | yes | calib | 9 | 16 | 1 |
| t453 | science-engineering | no | no | yes | calib | 10 | 16 | 0 |
| t454 | science-physics | yes | yes | yes | calib | 9 | 28 | 0 |
| t455 | puzzle-computed | no | no | yes | calib | 9 | 36 | 0 |
| t456 | science-chemistry | yes | no | **no** | calib | 7 | 20 | 5 |
| t457 | puzzle-computed | yes | yes | yes | calib | 8 | 21 | 5 |
| t458 | claim-verified | no | no | yes | calib | 9 | 26 | 8 |
| t459 | science-chemistry | yes | no | **no** | calib | 9 | 25 | 9 |
| t460 | claim-verified | yes | yes | yes | calib | 8 | 23 | 0 |
| t461 | science-biology | yes | no | **no** | calib | 10 | 21 | 3 |
| t462 | claim-verified | no | no | yes | calib | 8 | 12 | 0 |
| t463 | science-engineering | yes | yes | yes | calib | 9 | 23 | 0 |
| t464 | puzzle-computed | yes | yes | yes | calib | 9 | 31 | 14 |
| t465 | science-biology | yes | no | **no** | calib | 9 | 21 | 2 |
| t466 | puzzle-computed | yes | yes | yes | calib | 9 | 26 | 2 |
| t467 | simpleqa | yes | yes | yes | calib | 9 | 26 | 12 |
| t468 | claim-verified | no | no | yes | calib | 8 | 13 | 0 |
| t469 | simpleqa | no | no | yes | calib | 8 | 12 | 0 |
| t470 | science-engineering | no | no | yes | calib | 9 | 19 | 3 |
| t471 | puzzle-computed | no | no | yes | calib | 8 | 24 | 4 |
| t472 | science-chemistry | no | no | yes | calib | 9 | 36 | 0 |
| t473 | simpleqa | yes | yes | yes | calib | 8 | 17 | 6 |
| t474 | science-chemistry | no | no | yes | calib | 8 | 18 | 0 |
| t475 | science-engineering | yes | no | **no** | calib | 10 | 21 | 3 |
| t476 | simpleqa | no | no | yes | calib | 8 | 10 | 0 |
| t477 | science-biology | yes | yes | yes | calib | 8 | 27 | 0 |
| t478 | claim-verified | no | no | yes | calib | 10 | 19 | 1 |
| t479 | science-engineering | yes | no | **no** | calib | 9 | 17 | 0 |
| t480 | simpleqa | no | no | yes | calib | 9 | 24 | 0 |
| t481 | puzzle-computed | yes | yes | yes | calib | 9 | 19 | 0 |
| t482 | simpleqa | yes | no | **no** | calib | 9 | 32 | 7 |
| t483 | science-chemistry | no | no | yes | calib | 8 | 18 | 0 |
| t484 | puzzle-computed | no | no | yes | calib | 7 | 11 | 0 |
| t485 | science-physics | yes | no | **no** | calib | 8 | 17 | 5 |
| t486 | science-physics | no | no | yes | calib | 9 | 19 | 3 |
| t487 | simpleqa | no | no | yes | calib | 8 | 24 | 1 |
| t488 | simpleqa | no | no | yes | calib | 9 | 22 | 8 |
| t489 | puzzle-computed | no | no | yes | calib | 8 | 15 | 0 |
| t490 | science-engineering | no | no | yes | calib | 10 | 19 | 6 |
| t491 | puzzle-computed | no | no | yes | calib | 8 | 17 | 0 |
| t492 | science-physics | yes | yes | yes | calib | 8 | 19 | 4 |
| t493 | simpleqa | yes | no | **no** | calib | 9 | 13 | 0 |
| t494 | puzzle-computed | yes | yes | yes | calib | 9 | 21 | 5 |
| t495 | puzzle-computed | no | no | yes | calib | 8 | 17 | 6 |
| t496 | claim-verified | no | no | yes | calib | 9 | 16 | 1 |
| t497 | science-physics | no | no | yes | calib | 8 | 17 | 0 |
| t498 | claim-verified | yes | yes | yes | calib | 8 | 15 | 0 |
| t499 | claim-verified | no | no | yes | calib | 8 | 21 | 10 |
| t500 | simpleqa | no | no | yes | calib | 8 | 21 | 0 |
| t501 | claim-verified | no | no | yes | calib | 8 | 18 | 0 |
| t502 | claim-verified | no | no | yes | calib | 9 | 26 | 0 |
| t503 | puzzle-computed | yes | yes | yes | calib | 7 | 17 | 5 |
| t504 | claim-verified | yes | yes | yes | calib | 9 | 26 | 4 |
| t505 | puzzle-computed | yes | yes | yes | calib | 8 | 18 | 0 |
| t506 | science-engineering | no | no | yes | calib | 9 | 21 | 0 |
| t507 | puzzle-computed | yes | yes | yes | calib | 8 | 11 | 0 |
| t508 | puzzle-computed | yes | yes | yes | calib | 9 | 16 | 1 |
| t509 | simpleqa | no | no | yes | calib | 8 | 18 | 0 |
| t510 | simpleqa | yes | yes | yes | calib | 8 | 14 | 4 |
| t511 | simpleqa | yes | no | **no** | calib | 8 | 22 | 8 |
| t512 | puzzle-computed | no | no | yes | calib | 9 | 18 | 1 |
| t513 | puzzle-computed | yes | yes | yes | calib | 8 | 12 | 0 |
| t514 | puzzle-computed | no | no | yes | calib | 8 | 13 | 0 |
| t515 | science-engineering | yes | no | **no** | calib | 10 | 25 | 2 |
| t516 | simpleqa | yes | yes | yes | calib | 9 | 25 | 12 |
| t517 | science-chemistry | no | no | yes | calib | 8 | 28 | 0 |
| t518 | puzzle-computed | no | no | yes | calib | 8 | 25 | 6 |
| t519 | puzzle-computed | yes | yes | yes | calib | 11 | 31 | 0 |
| t520 | puzzle-computed | yes | yes | yes | calib | 8 | 16 | 4 |
| t521 | science-physics | yes | yes | yes | calib | 9 | 29 | 9 |
| t522 | claim-verified | no | no | yes | calib | 8 | 28 | 0 |
| t523 | simpleqa | no | no | yes | calib | 8 | 19 | 6 |
| t524 | puzzle-computed | no | no | yes | calib | 8 | 19 | 5 |
| t525 | puzzle-computed | no | no | yes | calib | 9 | 27 | 10 |
| t526 | science-engineering | yes | yes | yes | calib | 9 | 16 | 5 |
| t527 | simpleqa | yes | no | **no** | calib | 8 | 17 | 7 |
| t528 | science-chemistry | yes | yes | yes | calib | 8 | 13 | 0 |
| t529 | puzzle-computed | no | no | yes | calib | 9 | 28 | 8 |
| t530 | claim-verified | yes | yes | yes | calib | 8 | 20 | 8 |
| t531 | science-chemistry | yes | yes | yes | calib | 9 | 16 | 2 |
| t532 | simpleqa | yes | yes | yes | calib | 8 | 24 | 3 |
| t533 | science-physics | yes | no | **no** | calib | 9 | 21 | 5 |
| t534 | simpleqa | yes | yes | yes | calib | 9 | 23 | 2 |
| t535 | claim-verified | yes | yes | yes | calib | 8 | 11 | 1 |
| t536 | simpleqa | yes | no | **no** | calib | 10 | 13 | 1 |
| t537 | science-chemistry | yes | yes | yes | calib | 10 | 27 | 0 |
| t538 | science-physics | no | no | yes | calib | 9 | 29 | 8 |
| t539 | science-chemistry | no | yes | **no** | calib | 9 | 27 | 6 |
| t540 | science-biology | no | no | yes | calib | 9 | 33 | 5 |
| t541 | claim-verified | yes | yes | yes | calib | 9 | 25 | 2 |
| t542 | simpleqa | yes | no | **no** | calib | 8 | 12 | 5 |
| t543 | claim-verified | yes | yes | yes | calib | 8 | 18 | 0 |
| t544 | claim-verified | no | no | yes | calib | 10 | 27 | 8 |
| t545 | simpleqa | no | yes | **no** | calib | 10 | 36 | 20 |
| t546 | simpleqa | yes | no | **no** | calib | 9 | 21 | 0 |
| t547 | claim-verified | no | no | yes | calib | 9 | 19 | 0 |
| t548 | science-chemistry | yes | no | **no** | calib | 8 | 20 | 1 |
| t549 | simpleqa | no | no | yes | calib | 8 | 13 | 5 |
| t550 | puzzle-computed | no | no | yes | calib | 9 | 30 | 7 |
| t551 | science-biology | yes | yes | yes | calib | 9 | 17 | 6 |
| t552 | science-biology | no | no | yes | calib | 11 | 30 | 6 |
| t553 | science-chemistry | no | no | yes | calib | 9 | 25 | 9 |
| t554 | science-engineering | no | no | yes | calib | 9 | 15 | 0 |
| t555 | puzzle-computed | yes | yes | yes | calib | 10 | 29 | 5 |
| t556 | claim-verified | no | no | yes | calib | 9 | 23 | 0 |
| t557 | puzzle-computed | no | no | yes | calib | 10 | 35 | 12 |
| t558 | simpleqa | no | no | yes | calib | 9 | 21 | 0 |
| t559 | simpleqa | no | no | yes | calib | 8 | 11 | 0 |
| t560 | puzzle-computed | no | no | yes | calib | 7 | 19 | 0 |
| t561 | science-engineering | no | no | yes | calib | 9 | 27 | 5 |
| t562 | simpleqa | no | no | yes | calib | 8 | 14 | 4 |
| t563 | science-engineering | no | no | yes | calib | 8 | 21 | 0 |
| t564 | simpleqa | yes | no | **no** | calib | 9 | 25 | 6 |
| t565 | claim-verified | yes | yes | yes | calib | 9 | 24 | 0 |
| t566 | puzzle-computed | no | no | yes | calib | 10 | 26 | 1 |
| t567 | claim-verified | no | no | yes | calib | 8 | 17 | 4 |
| t568 | claim-verified | no | no | yes | calib | 9 | 24 | 10 |
| t569 | science-biology | yes | yes | yes | calib | 8 | 19 | 9 |
| t570 | simpleqa | yes | yes | yes | calib | 7 | 15 | 7 |
| t571 | simpleqa | no | no | yes | calib | 8 | 20 | 7 |
| t572 | claim-verified | no | no | yes | calib | 9 | 21 | 6 |
| t573 | science-biology | yes | yes | yes | calib | 10 | 25 | 4 |
| t574 | simpleqa | no | no | yes | calib | 8 | 20 | 4 |
| t575 | claim-verified | no | no | yes | calib | 8 | 20 | 0 |
| t576 | science-chemistry | yes | yes | yes | calib | 10 | 28 | 12 |
| t577 | claim-verified | no | no | yes | calib | 9 | 36 | 0 |
| t578 | science-biology | no | no | yes | calib | 9 | 23 | 8 |
| t579 | simpleqa | yes | no | **no** | calib | 9 | 23 | 11 |
| t580 | claim-verified | yes | yes | yes | calib | 10 | 17 | 1 |
| t581 | science-physics | yes | yes | yes | calib | 7 | 13 | 1 |
| t582 | puzzle-computed | no | no | yes | calib | 9 | 18 | 5 |
| t583 | claim-verified | no | no | yes | calib | 9 | 18 | 5 |
| t584 | claim-verified | no | no | yes | calib | 8 | 27 | 0 |
| t585 | science-chemistry | no | no | yes | calib | 9 | 30 | 8 |
| t586 | science-engineering | yes | yes | yes | calib | 8 | 18 | 0 |
| t587 | science-physics | no | no | yes | calib | 10 | 19 | 1 |
| t588 | puzzle-computed | yes | yes | yes | calib | 8 | 20 | 0 |
| t589 | simpleqa | yes | yes | yes | calib | 9 | 35 | 6 |
| t590 | simpleqa | yes | no | **no** | calib | 10 | 28 | 9 |
| t591 | simpleqa | no | no | yes | calib | 9 | 36 | 0 |
| t592 | science-chemistry | yes | yes | yes | calib | 9 | 26 | 3 |
| t593 | science-engineering | yes | no | **no** | calib | 10 | 23 | 0 |
| t594 | science-engineering | no | no | yes | calib | 10 | 26 | 4 |
| t595 | simpleqa | no | no | yes | calib | 10 | 24 | 0 |
| t596 | puzzle-computed | no | no | yes | calib | 8 | 19 | 1 |
| t597 | science-physics | yes | yes | yes | calib | 9 | 15 | 2 |
| t598 | science-engineering | yes | no | **no** | calib | 10 | 28 | 0 |
| t599 | science-physics | yes | no | **no** | calib | 9 | 27 | 10 |
| t600 | science-engineering | no | no | yes | calib | 7 | 21 | 0 |
| t601 | simpleqa | yes | no | **no** | calib | 8 | 16 | 6 |
| t602 | science-physics | no | no | yes | calib | 8 | 14 | 0 |
| t603 | simpleqa | no | no | yes | calib | 9 | 16 | 5 |
| t604 | simpleqa | no | no | yes | calib | 9 | 24 | 8 |
| t605 | science-engineering | yes | yes | yes | calib | 7 | 13 | 2 |
| t606 | simpleqa | no | no | yes | calib | 10 | 27 | 7 |
| t607 | science-chemistry | yes | yes | yes | calib | 10 | 21 | 4 |
| t608 | simpleqa | no | no | yes | calib | 8 | 16 | 0 |
| t609 | simpleqa | yes | yes | yes | calib | 10 | 31 | 12 |
| t610 | science-engineering | no | no | yes | calib | 8 | 22 | 9 |
| t611 | science-physics | no | no | yes | calib | 9 | 36 | 0 |
| t612 | science-physics | yes | yes | yes | calib | 8 | 16 | 2 |
| t613 | science-engineering | yes | no | **no** | calib | 8 | 14 | 5 |
| t614 | simpleqa | yes | no | **no** | calib | 9 | 14 | 5 |
| t615 | science-physics | no | no | yes | calib | 8 | 28 | 0 |
| t616 | science-chemistry | yes | no | **no** | calib | 9 | 25 | 0 |
| t617 | science-physics | no | no | yes | calib | 7 | 17 | 6 |
| t618 | science-physics | yes | yes | yes | calib | 9 | 21 | 4 |
| t619 | science-chemistry | no | no | yes | calib | 8 | 20 | 0 |
| t620 | simpleqa | no | no | yes | calib | 8 | 15 | 4 |
| t621 | science-chemistry | yes | yes | yes | calib | 8 | 18 | 1 |
| t622 | simpleqa | no | no | yes | calib | 8 | 23 | 0 |
| t623 | science-engineering | yes | no | **no** | calib | 9 | 26 | 0 |
| t624 | science-chemistry | yes | yes | yes | calib | 7 | 16 | 0 |
| t625 | science-chemistry | yes | yes | yes | calib | 9 | 29 | 8 |
| t626 | science-physics | no | no | yes | calib | 8 | 19 | 0 |
| t627 | science-engineering | no | no | yes | calib | 9 | 24 | 0 |
| t628 | science-engineering | yes | no | **no** | calib | 8 | 20 | 6 |
| t629 | simpleqa | no | no | yes | calib | 8 | 10 | 0 |
| t630 | simpleqa | no | no | yes | calib | 7 | 15 | 1 |
| t631 | science-engineering | no | no | yes | calib | 9 | 29 | 6 |
| t632 | science-chemistry | yes | no | **no** | calib | 10 | 32 | 0 |
| t633 | simpleqa | yes | yes | yes | calib | 9 | 26 | 8 |
| t634 | simpleqa | no | yes | **no** | calib | 9 | 22 | 10 |
| t635 | simpleqa | no | no | yes | calib | 8 | 14 | 0 |
| t636 | simpleqa | no | no | yes | calib | 8 | 16 | 0 |
| t637 | science-engineering | yes | yes | yes | calib | 9 | 23 | 8 |
| t638 | science-chemistry | no | no | yes | calib | 8 | 21 | 0 |
| t639 | science-engineering | no | no | yes | calib | 8 | 21 | 7 |
| t640 | science-physics | yes | yes | yes | calib | 8 | 20 | 2 |
| t641 | science-engineering | no | no | yes | calib | 10 | 24 | 7 |
| t642 | science-engineering | no | no | yes | calib | 11 | 30 | 7 |
| t643 | science-chemistry | no | no | yes | calib | 8 | 22 | 0 |
| t644 | science-engineering | yes | yes | yes | calib | 9 | 31 | 11 |
| t645 | science-engineering | no | no | yes | calib | 9 | 36 | 0 |
| t646 | science-physics | yes | no | **no** | calib | 10 | 28 | 0 |
| t647 | simpleqa | no | yes | **no** | calib | 9 | 14 | 6 |
| t648 | science-chemistry | yes | no | **no** | calib | 10 | 22 | 5 |
| t649 | science-chemistry | no | no | yes | calib | 10 | 39 | 0 |
| t650 | science-physics | no | no | yes | calib | 8 | 28 | 12 |
| t651 | science-chemistry | yes | yes | yes | calib | 9 | 23 | 7 |
| t652 | science-physics | no | no | yes | calib | 9 | 19 | 9 |
| t653 | simpleqa | no | no | yes | calib | 9 | 21 | 0 |
| t654 | science-physics | yes | no | **no** | calib | 9 | 26 | 2 |
| t655 | science-engineering | yes | yes | yes | calib | 8 | 20 | 4 |
| t656 | science-engineering | yes | yes | yes | calib | 10 | 27 | 1 |
| t657 | simpleqa | yes | no | **no** | calib | 10 | 18 | 7 |
| t658 | science-chemistry | no | no | yes | calib | 8 | 17 | 2 |
| t659 | science-engineering | yes | no | **no** | calib | 10 | 28 | 8 |
| t660 | science-chemistry | no | no | yes | calib | 7 | 16 | 0 |
| t661 | science-physics | yes | yes | yes | calib | 8 | 19 | 4 |
| t662 | science-physics | yes | yes | yes | calib | 9 | 31 | 0 |
| t663 | simpleqa | yes | no | **no** | calib | 10 | 31 | 4 |
| t664 | science-chemistry | no | no | yes | calib | 8 | 26 | 4 |
| t665 | science-engineering | yes | yes | yes | calib | 8 | 16 | 1 |
| t666 | science-chemistry | no | no | yes | calib | 8 | 23 | 7 |
| t667 | science-engineering | yes | yes | yes | calib | 10 | 39 | 0 |
| t668 | science-engineering | no | no | yes | calib | 9 | 27 | 12 |
| t669 | science-chemistry | yes | yes | yes | calib | 10 | 26 | 5 |
| t670 | science-chemistry | no | no | yes | calib | 8 | 21 | 3 |
| t671 | science-physics | yes | yes | yes | calib | 8 | 21 | 5 |
| t672 | science-engineering | no | no | yes | calib | 8 | 25 | 0 |
| t673 | science-physics | no | no | yes | calib | 9 | 19 | 0 |
| t674 | simpleqa | no | no | yes | calib | 9 | 14 | 5 |
| t675 | simpleqa | yes | no | **no** | calib | 10 | 24 | 5 |
| t676 | science-chemistry | yes | yes | yes | calib | 7 | 21 | 0 |
| t677 | science-physics | yes | yes | yes | calib | 8 | 28 | 0 |
| t678 | science-physics | yes | yes | yes | calib | 7 | 10 | 0 |
| t679 | science-chemistry | yes | yes | yes | calib | 9 | 36 | 0 |
| t680 | science-physics | yes | yes | yes | calib | 9 | 20 | 5 |
| t681 | science-physics | yes | yes | yes | calib | 8 | 27 | 0 |
| t682 | science-chemistry | yes | yes | yes | calib | 8 | 15 | 0 |
| t683 | science-physics | yes | yes | yes | calib | 9 | 19 | 0 |
| t684 | science-physics | no | no | yes | calib | 8 | 24 | 0 |
| t685 | simpleqa | yes | yes | yes | calib | 8 | 18 | 5 |
| t686 | simpleqa | no | no | yes | calib | 7 | 14 | 3 |
| t687 | science-physics | no | no | yes | calib | 8 | 19 | 0 |
| t688 | science-engineering | yes | no | **no** | calib | 9 | 29 | 4 |
| t689 | science-engineering | no | no | yes | calib | 7 | 13 | 0 |
| t690 | simpleqa | yes | yes | yes | calib | 8 | 13 | 5 |
| t691 | science-physics | yes | yes | yes | calib | 9 | 23 | 7 |
| t692 | simpleqa | yes | yes | yes | calib | 8 | 16 | 0 |
| t693 | science-chemistry | no | no | yes | calib | 8 | 28 | 7 |
| t694 | science-chemistry | no | no | yes | calib | 8 | 18 | 0 |
| t695 | science-physics | no | no | yes | calib | 8 | 21 | 8 |
| t696 | science-physics | no | no | yes | calib | 8 | 19 | 2 |
| t697 | science-engineering | no | no | yes | calib | 9 | 23 | 6 |
| t698 | science-physics | yes | yes | yes | calib | 6 | 10 | 0 |
| t699 | science-physics | yes | yes | yes | calib | 8 | 17 | 3 |
| t700 | science-physics | no | no | yes | calib | 8 | 15 | 0 |
| t701 | science-chemistry | no | no | yes | calib | 9 | 11 | 1 |
| t702 | simpleqa | yes | no | **no** | calib | 10 | 30 | 8 |
| t703 | simpleqa | no | no | yes | calib | 7 | 18 | 0 |
| t704 | science-chemistry | no | no | yes | calib | 9 | 24 | 3 |
| t705 | science-chemistry | no | no | yes | calib | 8 | 24 | 6 |
| t706 | science-chemistry | yes | yes | yes | calib | 7 | 14 | 0 |
| t707 | simpleqa | yes | yes | yes | calib | 10 | 33 | 9 |
| t708 | science-engineering | yes | yes | yes | calib | 8 | 16 | 1 |
| t709 | science-chemistry | no | no | yes | calib | 9 | 22 | 4 |
| t710 | simpleqa | no | yes | **no** | calib | 9 | 20 | 6 |
| t711 | science-chemistry | yes | yes | yes | calib | 9 | 29 | 6 |
| t712 | science-engineering | no | no | yes | calib | 9 | 25 | 0 |
| t713 | science-physics | yes | no | **no** | calib | 9 | 21 | 0 |
| t714 | science-engineering | no | no | yes | calib | 8 | 14 | 6 |
| t715 | simpleqa | yes | no | **no** | calib | 9 | 15 | 3 |
| t716 | science-engineering | no | yes | **no** | calib | 10 | 16 | 1 |
| t717 | science-chemistry | yes | no | **no** | calib | 9 | 27 | 0 |
| t718 | science-chemistry | yes | yes | yes | calib | 9 | 22 | 0 |
| t719 | science-engineering | yes | yes | yes | calib | 9 | 21 | 0 |
| t720 | simpleqa | no | no | yes | calib | 8 | 25 | 0 |
| t721 | science-engineering | yes | yes | yes | calib | 10 | 25 | 0 |
| t722 | science-physics | yes | yes | yes | calib | 9 | 17 | 5 |
| t723 | science-chemistry | no | no | yes | calib | 10 | 31 | 5 |
| t724 | science-physics | no | no | yes | calib | 7 | 21 | 0 |
| t725 | science-engineering | yes | yes | yes | calib | 9 | 23 | 0 |
| t726 | science-physics | no | no | yes | calib | 9 | 19 | 1 |
| t727 | simpleqa | no | yes | **no** | calib | 9 | 14 | 7 |
| t728 | science-physics | yes | yes | yes | calib | 10 | 18 | 3 |
| t729 | simpleqa | no | no | yes | calib | 9 | 25 | 0 |
| t730 | simpleqa | yes | no | **no** | calib | 8 | 17 | 6 |
| t731 | science-engineering | yes | yes | yes | calib | 10 | 36 | 7 |
| t732 | simpleqa | no | no | yes | calib | 9 | 22 | 3 |
| t733 | simpleqa | no | no | yes | calib | 8 | 21 | 6 |
| t734 | science-physics | no | no | yes | calib | 7 | 16 | 0 |
| t735 | simpleqa | no | no | yes | calib | 9 | 20 | 1 |
| t736 | simpleqa | yes | yes | yes | calib | 8 | 16 | 6 |
| t737 | science-physics | yes | no | **no** | calib | 8 | 23 | 4 |
| t738 | science-physics | no | no | yes | calib | 9 | 32 | 0 |
| t739 | science-engineering | no | no | yes | calib | 10 | 27 | 8 |
| t740 | simpleqa | yes | no | **no** | calib | 9 | 25 | 13 |
| t741 | simpleqa | no | no | yes | calib | 9 | 20 | 0 |
| t742 | simpleqa | yes | no | **no** | calib | 9 | 14 | 7 |
| t743 | simpleqa | yes | yes | yes | calib | 10 | 21 | 5 |
| t744 | science-physics | yes | yes | yes | calib | 8 | 15 | 4 |
| t745 | science-physics | no | no | yes | calib | 9 | 20 | 2 |
| t746 | science-physics | no | no | yes | calib | 8 | 19 | 0 |
| t747 | science-chemistry | yes | yes | yes | calib | 9 | 23 | 3 |
| t748 | science-chemistry | yes | no | **no** | calib | 10 | 28 | 3 |
| t749 | simpleqa | no | no | yes | calib | 9 | 27 | 1 |
| t750 | science-chemistry | yes | yes | yes | calib | 9 | 22 | 0 |
| t751 | simpleqa | yes | yes | yes | calib | 8 | 16 | 4 |
| t752 | science-chemistry | no | no | yes | calib | 9 | 29 | 8 |
| t753 | science-engineering | yes | yes | yes | calib | 8 | 17 | 0 |
| t754 | simpleqa | no | no | yes | calib | 9 | 26 | 7 |
| t755 | simpleqa | yes | no | **no** | calib | 9 | 29 | 7 |
| t756 | science-engineering | yes | yes | yes | calib | 8 | 23 | 6 |
| t757 | science-physics | yes | yes | yes | calib | 8 | 17 | 4 |
| t758 | science-physics | yes | no | **no** | calib | 9 | 23 | 4 |
| t759 | simpleqa | no | no | yes | calib | 8 | 25 | 6 |
| t760 | simpleqa | yes | no | **no** | calib | 10 | 25 | 4 |
| t761 | simpleqa | yes | yes | yes | calib | 8 | 10 | 2 |
| t762 | science-engineering | yes | yes | yes | calib | 9 | 20 | 0 |
| t763 | science-physics | no | no | yes | calib | 8 | 24 | 0 |
| t764 | science-physics | no | no | yes | calib | 9 | 30 | 7 |
| t765 | science-physics | yes | no | **no** | calib | 8 | 19 | 2 |
| t766 | science-engineering | yes | no | **no** | calib | 11 | 33 | 10 |
| t767 | simpleqa | yes | no | **no** | calib | 9 | 12 | 3 |
| t768 | simpleqa | yes | yes | yes | calib | 10 | 27 | 12 |
| t769 | simpleqa | no | no | yes | calib | 9 | 15 | 5 |
| t770 | simpleqa | yes | yes | yes | calib | 9 | 16 | 0 |
| t771 | simpleqa | no | yes | **no** | calib | 8 | 19 | 9 |
| t772 | science-chemistry | yes | no | **no** | calib | 7 | 14 | 3 |
| t773 | science-chemistry | no | no | yes | calib | 8 | 20 | 0 |
| t774 | science-physics | no | no | yes | calib | 8 | 20 | 0 |
| t775 | simpleqa | no | no | yes | calib | 8 | 22 | 0 |
| t776 | science-physics | no | no | yes | calib | 9 | 34 | 9 |
| t777 | simpleqa | no | yes | **no** | calib | 8 | 16 | 3 |
| t778 | science-chemistry | yes | yes | yes | calib | 8 | 20 | 0 |
| t779 | science-chemistry | yes | yes | yes | calib | 8 | 17 | 5 |
| t780 | simpleqa | yes | no | **no** | calib | 8 | 15 | 8 |
| t781 | science-chemistry | yes | yes | yes | calib | 10 | 26 | 1 |
| t782 | science-physics | no | no | yes | calib | 8 | 22 | 4 |
| t783 | simpleqa | no | no | yes | calib | 9 | 19 | 8 |
| t784 | science-chemistry | yes | no | **no** | calib | 8 | 15 | 1 |
| t785 | science-chemistry | yes | yes | yes | calib | 8 | 21 | 10 |
| t786 | science-engineering | yes | yes | yes | calib | 8 | 13 | 2 |
| t787 | simpleqa | no | no | yes | calib | 6 | 14 | 0 |
| t788 | science-engineering | yes | yes | yes | calib | 9 | 27 | 1 |
| t789 | science-physics | no | no | yes | calib | 8 | 16 | 5 |
| t790 | simpleqa | yes | no | **no** | calib | 9 | 18 | 0 |
| t791 | science-chemistry | yes | yes | yes | calib | 9 | 20 | 6 |
| t792 | simpleqa | no | no | yes | calib | 8 | 23 | 2 |
| t793 | science-engineering | no | no | yes | calib | 10 | 28 | 0 |
| t794 | science-chemistry | yes | yes | yes | calib | 8 | 22 | 5 |
| t795 | science-physics | no | no | yes | calib | 9 | 28 | 6 |
| t796 | simpleqa | yes | yes | yes | calib | 9 | 18 | 4 |
| t797 | science-physics | no | no | yes | calib | 8 | 19 | 0 |
| t798 | science-chemistry | no | no | yes | calib | 9 | 22 | 0 |
| t799 | simpleqa | yes | no | **no** | calib | 10 | 16 | 9 |
| t800 | simpleqa | yes | yes | yes | calib | 10 | 9 | 3 |
| t801 | simpleqa | yes | no | **no** | calib | 8 | 20 | 5 |
| t802 | simpleqa | no | no | yes | calib | 9 | 19 | 6 |
| t803 | science-chemistry | no | no | yes | calib | 9 | 22 | 0 |
| t804 | science-physics | yes | no | **no** | calib | 9 | 18 | 4 |
| t805 | science-engineering | no | no | yes | calib | 10 | 36 | 0 |
| t806 | science-physics | no | no | yes | calib | 8 | 22 | 3 |
| t807 | science-chemistry | no | no | yes | calib | 9 | 17 | 0 |
| t808 | science-physics | yes | yes | yes | calib | 10 | 22 | 6 |
| t809 | science-physics | yes | yes | yes | calib | 9 | 26 | 11 |
| t810 | science-physics | no | no | yes | calib | 7 | 17 | 4 |
| t811 | science-chemistry | no | no | yes | calib | 7 | 12 | 4 |
| t812 | science-physics | yes | yes | yes | calib | 8 | 23 | 3 |
| t813 | science-engineering | no | no | yes | calib | 9 | 18 | 0 |
| t814 | simpleqa | yes | no | **no** | calib | 8 | 24 | 7 |
| t815 | science-engineering | no | no | yes | calib | 10 | 30 | 0 |
| t816 | science-engineering | no | no | yes | calib | 10 | 23 | 0 |
| t817 | simpleqa | yes | yes | yes | calib | 10 | 20 | 6 |
| t818 | science-engineering | no | no | yes | calib | 9 | 23 | 9 |
| t819 | science-engineering | yes | yes | yes | calib | 9 | 29 | 1 |
| t820 | science-chemistry | no | no | yes | calib | 8 | 17 | 0 |
| t821 | science-engineering | yes | no | **no** | calib | 9 | 25 | 0 |
| t822 | science-physics | yes | yes | yes | calib | 9 | 32 | 5 |
| t823 | simpleqa | yes | no | **no** | calib | 9 | 17 | 3 |
| t824 | science-engineering | yes | yes | yes | calib | 8 | 20 | 0 |
| t825 | science-engineering | no | no | yes | calib | 9 | 22 | 0 |
| t826 | simpleqa | yes | yes | yes | calib | 8 | 16 | 8 |
| t827 | simpleqa | yes | yes | yes | calib | 10 | 32 | 15 |
| t828 | science-chemistry | no | no | yes | calib | 8 | 16 | 0 |
| t829 | simpleqa | yes | no | **no** | calib | 9 | 19 | 4 |
| t830 | science-engineering | no | no | yes | calib | 9 | 26 | 0 |
| t831 | simpleqa | yes | yes | yes | calib | 9 | 35 | 14 |
| t832 | science-engineering | no | no | yes | calib | 8 | 15 | 2 |
| t833 | simpleqa | no | no | yes | calib | 7 | 13 | 6 |
| t834 | science-chemistry | yes | yes | yes | calib | 10 | 32 | 0 |
| t835 | science-chemistry | yes | no | **no** | calib | 9 | 24 | 7 |
| t836 | science-engineering | yes | no | **no** | calib | 9 | 30 | 12 |
| t837 | science-engineering | yes | yes | yes | calib | 10 | 25 | 2 |
| t838 | science-physics | yes | yes | yes | calib | 9 | 26 | 0 |
| t839 | simpleqa | yes | yes | yes | calib | 9 | 22 | 8 |
| t840 | science-physics | no | no | yes | calib | 8 | 17 | 0 |
| t841 | science-engineering | yes | no | **no** | calib | 8 | 22 | 1 |
| t842 | science-engineering | no | no | yes | calib | 9 | 23 | 0 |
| t843 | simpleqa | no | no | yes | calib | 8 | 16 | 0 |
| t844 | science-chemistry | no | no | yes | calib | 9 | 15 | 0 |
| t845 | simpleqa | no | no | yes | calib | 9 | 23 | 2 |
| t846 | simpleqa | yes | yes | yes | calib | 9 | 21 | 8 |
| t847 | science-engineering | no | no | yes | calib | 8 | 17 | 7 |
| t848 | science-physics | yes | yes | yes | calib | 9 | 18 | 2 |
| t849 | science-engineering | no | no | yes | calib | 8 | 15 | 3 |
| t850 | science-engineering | yes | yes | yes | calib | 8 | 13 | 0 |
| t851 | simpleqa | no | no | yes | calib | 8 | 23 | 0 |
| t852 | science-physics | yes | yes | yes | calib | 10 | 25 | 8 |
| t853 | science-physics | no | no | yes | calib | 9 | 31 | 4 |
| t854 | simpleqa | yes | yes | yes | calib | 9 | 22 | 8 |
| t855 | science-chemistry | no | no | yes | calib | 9 | 21 | 0 |
| t856 | simpleqa | yes | no | **no** | calib | 10 | 17 | 8 |
| t857 | science-chemistry | no | no | yes | calib | 10 | 45 | 0 |
| t858 | simpleqa | yes | yes | yes | calib | 8 | 22 | 8 |
| t859 | simpleqa | yes | yes | yes | calib | 8 | 21 | 9 |
| t860 | science-engineering | yes | no | **no** | calib | 8 | 14 | 5 |
| t861 | simpleqa | no | no | yes | calib | 8 | 21 | 0 |
| t862 | science-chemistry | no | no | yes | calib | 9 | 23 | 0 |
| t863 | simpleqa | no | no | yes | calib | 8 | 17 | 0 |
| t864 | simpleqa | no | no | yes | calib | 8 | 13 | 0 |
| t865 | science-engineering | yes | no | **no** | calib | 9 | 20 | 0 |
| t866 | science-engineering | yes | no | **no** | calib | 10 | 28 | 0 |
| t867 | science-chemistry | no | no | yes | calib | 9 | 26 | 0 |
| t868 | science-chemistry | yes | yes | yes | calib | 8 | 28 | 0 |
| t869 | science-engineering | yes | yes | yes | calib | 7 | 15 | 3 |
| t870 | science-physics | yes | yes | yes | calib | 8 | 16 | 1 |
| t871 | science-engineering | no | no | yes | calib | 8 | 16 | 0 |
| t872 | simpleqa | yes | yes | yes | calib | 9 | 26 | 7 |
| t873 | simpleqa | yes | yes | yes | calib | 10 | 27 | 10 |
| t874 | science-physics | no | no | yes | calib | 9 | 27 | 11 |
| t875 | science-chemistry | yes | no | **no** | calib | 10 | 27 | 6 |
| t876 | science-chemistry | yes | yes | yes | calib | 7 | 11 | 0 |
| t877 | simpleqa | no | yes | **no** | calib | 9 | 14 | 4 |
| t878 | science-chemistry | no | no | yes | calib | 7 | 20 | 0 |
| t879 | simpleqa | no | no | yes | calib | 10 | 24 | 8 |
| t880 | science-engineering | no | no | yes | calib | 10 | 20 | 1 |
| t881 | science-engineering | no | no | yes | calib | 8 | 22 | 0 |
| t882 | science-chemistry | yes | yes | yes | calib | 9 | 21 | 0 |
| t883 | science-engineering | no | no | yes | calib | 8 | 19 | 1 |
| t884 | science-physics | no | no | yes | calib | 9 | 15 | 0 |
| t885 | simpleqa | no | no | yes | calib | 8 | 16 | 0 |
| t886 | simpleqa | no | no | yes | calib | 7 | 11 | 1 |
| t887 | science-chemistry | no | no | yes | calib | 10 | 30 | 0 |
| t888 | science-chemistry | no | no | yes | calib | 8 | 19 | 6 |
| t889 | science-engineering | yes | yes | yes | calib | 9 | 21 | 0 |
| t890 | simpleqa | no | no | yes | calib | 9 | 27 | 0 |
| t891 | simpleqa | yes | yes | yes | calib | 8 | 17 | 7 |
| t892 | science-physics | no | no | yes | calib | 8 | 23 | 8 |
| t893 | simpleqa | no | no | yes | calib | 7 | 11 | 2 |
| t894 | science-chemistry | yes | yes | yes | calib | 10 | 38 | 7 |
| t895 | science-physics | no | no | yes | calib | 8 | 22 | 0 |
| t896 | simpleqa | yes | no | **no** | calib | 8 | 12 | 2 |
| t897 | science-engineering | yes | yes | yes | calib | 9 | 22 | 4 |
| t898 | simpleqa | no | no | yes | calib | 8 | 18 | 3 |
| t899 | simpleqa | yes | no | **no** | calib | 9 | 27 | 11 |
| t900 | science-chemistry | no | no | yes | calib | 9 | 20 | 4 |
| t901 | science-engineering | no | no | yes | calib | 8 | 20 | 0 |
| t902 | science-physics | no | no | yes | calib | 8 | 17 | 0 |
| t903 | science-physics | yes | no | **no** | calib | 9 | 23 | 7 |
| t904 | science-engineering | no | no | yes | calib | 10 | 14 | 0 |
| t905 | science-engineering | no | no | yes | calib | 9 | 31 | 0 |
| t906 | simpleqa | no | no | yes | calib | 9 | 12 | 4 |
| t907 | simpleqa | yes | yes | yes | calib | 7 | 11 | 5 |
| t908 | science-physics | no | no | yes | calib | 8 | 22 | 5 |
| t909 | simpleqa | yes | yes | yes | calib | 8 | 18 | 8 |
| t910 | science-physics | no | no | yes | calib | 8 | 14 | 0 |
| t911 | science-physics | no | no | yes | calib | 9 | 21 | 5 |
| t912 | science-physics | yes | yes | yes | calib | 8 | 27 | 7 |
| t913 | science-chemistry | yes | yes | yes | calib | 8 | 19 | 0 |
| t914 | simpleqa | no | no | yes | calib | 9 | 17 | 0 |
| t915 | science-chemistry | yes | yes | yes | calib | 10 | 23 | 0 |
| t916 | science-chemistry | yes | yes | yes | calib | 8 | 22 | 0 |
| t917 | science-engineering | yes | yes | yes | calib | 9 | 25 | 0 |
| t918 | simpleqa | no | no | yes | calib | 9 | 13 | 1 |
| t919 | simpleqa | yes | no | **no** | calib | 8 | 13 | 3 |
| t920 | science-physics | no | no | yes | calib | 9 | 21 | 1 |
| t921 | science-chemistry | yes | yes | yes | calib | 9 | 22 | 7 |
| t922 | science-engineering | yes | yes | yes | calib | 8 | 28 | 0 |
| t923 | science-engineering | no | no | yes | calib | 10 | 24 | 0 |
| t924 | simpleqa | no | no | yes | calib | 9 | 9 | 0 |
| t925 | simpleqa | yes | no | **no** | calib | 7 | 7 | 0 |
| t926 | simpleqa | no | no | yes | calib | 10 | 24 | 6 |
| t927 | science-chemistry | no | no | yes | calib | 9 | 23 | 1 |
| t928 | science-chemistry | yes | yes | yes | calib | 9 | 22 | 1 |
| t929 | science-engineering | no | no | yes | calib | 11 | 20 | 1 |
| t930 | simpleqa | yes | yes | yes | calib | 9 | 18 | 4 |
| t931 | science-chemistry | no | no | yes | calib | 8 | 23 | 0 |
| t932 | simpleqa | yes | no | **no** | calib | 10 | 21 | 4 |
| t933 | science-physics | yes | no | **no** | calib | 9 | 20 | 2 |
| t934 | simpleqa | no | no | yes | calib | 8 | 18 | 6 |
| t935 | science-engineering | no | no | yes | calib | 9 | 26 | 0 |
| t936 | simpleqa | no | no | yes | calib | 8 | 17 | 7 |
| t937 | simpleqa | no | no | yes | calib | 10 | 23 | 4 |
| t938 | simpleqa | no | no | yes | calib | 9 | 17 | 1 |
| t939 | science-chemistry | no | no | yes | calib | 8 | 17 | 0 |
| t940 | simpleqa | no | yes | **no** | calib | 8 | 24 | 10 |
| t941 | science-chemistry | yes | no | **no** | calib | 8 | 19 | 0 |
| t942 | simpleqa | no | no | yes | calib | 10 | 24 | 5 |
| t943 | simpleqa | yes | no | **no** | calib | 10 | 25 | 1 |
| t944 | simpleqa | yes | no | **no** | calib | 9 | 19 | 7 |
| t945 | simpleqa | no | no | yes | calib | 8 | 23 | 6 |
| t946 | simpleqa | yes | yes | yes | calib | 8 | 13 | 8 |
| t947 | science-chemistry | no | no | yes | calib | 7 | 14 | 0 |
| t948 | science-chemistry | no | no | yes | calib | 8 | 22 | 0 |
| t949 | science-physics | no | no | yes | calib | 9 | 25 | 6 |
| t950 | science-chemistry | yes | no | **no** | calib | 8 | 17 | 0 |
| t951 | science-engineering | yes | yes | yes | calib | 9 | 18 | 0 |
| t952 | science-physics | yes | yes | yes | calib | 7 | 17 | 0 |
| t953 | science-engineering | no | no | yes | calib | 8 | 21 | 0 |
| t954 | science-engineering | yes | no | **no** | calib | 10 | 22 | 0 |
| t955 | science-engineering | yes | yes | yes | calib | 10 | 24 | 4 |
| t956 | science-engineering | yes | yes | yes | calib | 9 | 26 | 0 |
| t957 | science-engineering | no | no | yes | calib | 10 | 25 | 2 |
| t958 | science-engineering | yes | yes | yes | calib | 8 | 28 | 0 |
| t959 | science-physics | yes | yes | yes | calib | 9 | 17 | 1 |
| t960 | science-chemistry | yes | yes | yes | calib | 10 | 28 | 0 |
| t961 | simpleqa | no | no | yes | calib | 8 | 13 | 0 |
| t962 | science-physics | yes | yes | yes | calib | 8 | 23 | 4 |
| t963 | simpleqa | yes | yes | yes | calib | 9 | 23 | 5 |
| t964 | science-engineering | no | no | yes | calib | 9 | 15 | 0 |
| t965 | science-engineering | no | yes | **no** | calib | 8 | 24 | 11 |
| t966 | science-physics | yes | yes | yes | calib | 8 | 18 | 3 |
| t967 | science-physics | no | no | yes | calib | 9 | 30 | 0 |
| t968 | science-physics | yes | yes | yes | calib | 9 | 31 | 0 |
| t969 | science-chemistry | no | no | yes | calib | 9 | 32 | 0 |
| t970 | simpleqa | no | no | yes | calib | 8 | 24 | 5 |
| t971 | science-physics | yes | yes | yes | calib | 9 | 23 | 4 |
| t972 | simpleqa | yes | no | **no** | calib | 8 | 15 | 6 |
| t973 | simpleqa | no | no | yes | calib | 8 | 16 | 4 |
| t974 | science-physics | yes | yes | yes | calib | 10 | 23 | 3 |
| t975 | science-engineering | no | no | yes | calib | 8 | 15 | 1 |
| t976 | science-physics | yes | yes | yes | calib | 8 | 18 | 5 |
| t977 | simpleqa | yes | no | **no** | calib | 9 | 20 | 0 |
| t978 | simpleqa | yes | yes | yes | calib | 10 | 22 | 4 |
| t979 | science-chemistry | no | no | yes | calib | 8 | 20 | 0 |
| t980 | science-engineering | yes | yes | yes | calib | 9 | 29 | 0 |
| t981 | science-chemistry | no | no | yes | calib | 8 | 23 | 0 |
| t982 | simpleqa | no | no | yes | calib | 7 | 16 | 0 |
| t983 | simpleqa | yes | no | **no** | calib | 8 | 21 | 10 |
| t984 | simpleqa | no | no | yes | calib | 8 | 17 | 2 |
| t985 | science-engineering | no | no | yes | calib | 9 | 28 | 6 |
| t986 | science-chemistry | yes | yes | yes | calib | 8 | 28 | 0 |
| t987 | science-chemistry | yes | yes | yes | calib | 8 | 27 | 0 |
| t988 | simpleqa | no | no | yes | calib | 8 | 13 | 5 |
| t989 | science-engineering | no | no | yes | calib | 8 | 22 | 1 |
| t990 | science-engineering | yes | no | **no** | calib | 8 | 15 | 3 |
| t991 | simpleqa | yes | yes | yes | calib | 8 | 15 | 5 |
| t992 | simpleqa | yes | yes | yes | calib | 10 | 24 | 11 |
| t993 | science-engineering | yes | yes | yes | calib | 9 | 21 | 2 |
| t994 | science-chemistry | no | no | yes | calib | 7 | 16 | 0 |
| t995 | science-chemistry | no | no | yes | calib | 9 | 23 | 0 |
| t996 | science-chemistry | yes | yes | yes | calib | 9 | 18 | 3 |
| t997 | simpleqa | no | no | yes | calib | 8 | 14 | 5 |
| t998 | science-physics | no | no | yes | calib | 10 | 27 | 0 |
| t999 | science-engineering | yes | no | **no** | calib | 9 | 24 | 1 |

Wrong by category: claim-verified 0/98, puzzle-computed 0/150, science-biology 4/50, science-chemistry 21/150, science-engineering 31/150, science-physics 16/150, simpleqa 86/300


Wrong items:

- t017: A helical spring, having square and ground ends has a total of18 coils and its material has a modulus of elasticity in shearof 12 × 10^6 psi. Find out the maximum deflection that canbe produced in the spring due to a load of 90 lbs. if the springhas an outside diameter of 3.8 in. and an inside diameterof 0.25 in.
Is the correct answer "11 in."? (truth yes, model no)
- t030: Laminar film condensation of super-saturated steam occurs on a vertical surface. The steam is at a pressure of 1.43 psi and a saturation temperature of 114°F. If the wall temperature is 105°F, what is the coefficient of heat transfer at a point 3 in. from the top?
Is the correct answer "1,486 Btu/hr-ft^2-°F"? (truth no, model yes)
- t046: Light from the sun is reflected on a tiny plane mirror measuring 2 mm × 2 mm in size. What is the shape of the illuminated area on a screen (a) 1 cm away and (b) 2 m away from the mirror?
Is the correct answer "(a) rectangular, (b) circular"? (truth yes, model no)
- t048: Who voiced the character of Hercules in the 1978 animated television series "The Freedom Force"? Is the answer "Dida Ritz"? (truth no, model yes)
- t065: For the reaction 4C_2H_5Cl(g) + 13O_2(g) = 2 Cl_2 (g) + 8 CO_2 (g) + 10 H_2O (g) , \DeltaH_298°K = - 1229.6 kcal . Also, the heat of combustion per mole of C_2H_6 (g) to CO_2 (g) and H_2O (g) = - 341 kcal, the heat of formation per mole of H_2O (g) = - 57.8 kcal and the heat of formation per mole of HCl(g) = - 2.1 kcal. For the reaction C_2H_6 (g) + Cl_2 (g) = C_2H_5Cl(g) + HCl(g) (a) Calculate \DeltaH_298°K (b) Calculate \DeltaH_398°K for the first reaction assuming \DeltaC_P = - 10 cal/deg (c) Calculate \DeltaE_298°k for the first reaction
Is the correct answer "- 103 kcal, - 1230.6 kcal, - 1231.4 kcal"? (truth yes, model no)
- t078: In what city was the 6th ASEM Education Ministers' Meeting held? Is the answer "Seoul"? (truth yes, model no)
- t082: When using EIS with the Sigma FP, what is my maximum shutter speed? Is the answer "1/4,000 sec"? (truth yes, model no)
- t084: What minor planet designation number was originally assigned to the asteroid 176 Iduna? Is the answer "175"? (truth yes, model no)
- t1000: Which award did "The Bear" win in 2022? Is the answer "Top 10 Programs of the Year in American Film Institute Awards."? (truth yes, model no)
- t1012: A chemist has a solution which contains Zn^2+ and Cu^2+, each at .02M. If the solution is made 1M in H_3O+ and H_2S is bubbled in until the solution is saturated, will a precipitate form? K_sp of ZnS = 1 × 10-^22, K_sp of CuS = 8 × 10-^37, and K_eq for H_2S, when saturated, = 1 × 10-^22 .
Is the correct answer "Precipitation only at low pH values"? (truth no, model yes)
- t1013: Find the current that will flow in a series circuit contain-ing a 5-k\Omega resistor, a 470-\rhoF capacitor, a 150-mH inductor, and a 0.001\muF capacitor if the exciting voltage is 65V at 25-kHz.
Is the correct answer "10.5\angle- 36.3°mA"? (truth yes, model no)
- t1028: In a diode vacuum tube consisting of a heated, plane metal cathode and a parallel plate, electrons are emitted from the cathode and are accelerated toward the plate. In the region between the two tube elements there is a cloud of electrons called a space charge. The potential function is given by V = V_0 (x/a)^4/3, where V_0 is the potential of the plate, x is the coordinate distance from the cathode, and a is the distance of the plate from the cathode. Assuming that the electrons are emitted with negligible initial velocity, find the velocity of the electrons at any point x and the time of flight from cathode to plate.
Is the correct answer "time of flight = 5.5(10^-9) sec, velocity at plate = 5.93 (10^6) m per sec"? (truth yes, model no)
- t1032: What specific date (month, day, year) was the very first Q Con hosted by Prism Comics in West Hollywood? Is the answer "June 18, 2022"? (truth yes, model no)
- t1044: What EP did Milet release in 2021? Is the answer "Personification of destiny"? (truth no, model yes)
- t1047: In which year was the IFT Industrial Scientist Award, awarded by the Institute of Food Technologists for scientists, first awarded? Is the answer "1994"? (truth yes, model no)
- t105: What year was the municipality of Anorí, Antioquia, Colombia, founded? Is the answer "1858"? (truth no, model yes)
- t124: What were the day, month, and year when President Bush and Congress agreed on the joint resolution authorizing the Iraq War? Is the answer "October 2, 2002"? (truth yes, model no)
- t156: What profession did the father of Colombian mathematician and politician Sergio Fajardo Valderrama have? Is the answer "Architect"? (truth yes, model no)
- t160: What day, month, and year was the boxer Sergei Kobozev reported missing by his girlfriend? Is the answer "8 November 1995"? (truth yes, model no)
- t164: The dew point (the temperature at which the water vapor in a given sample of air becomes saturated and condensation be-comes possible) of a mass of air at 15°C is 10°C. Calculate the relative humidity and the mass of 1 liter of the moist air if the barometric height is 76 cm of mercury. The gram- molecular weight of air is 28.9 g and the saturated aqueous vapor pressures at 10°C and 15°C are 9.2 mm of mercury and 12.8 mm of mercury, respectively.
Is the correct answer "Relative Humidity: 71.9%, Mass of 1 liter moist air: 1.2346 g"? (truth yes, model no)
- t167: Which Victoria and Albert Museum director called it "an extremely capacious handbag"? Is the answer "Sir Roy Strong"? (truth yes, model no)
- t169: Which Terraria patch added the secret world seed Celebrationmk10? Is the answer "1.2.3"? (truth no, model yes)
- t171: Who designed Buenos Aires's Palais de Glace? Is the answer "J. E. H. Benoît"? (truth no, model yes)
- t198: In how many games did Matija Radović appear for the Hofstra Pride during the 2017-18 season? Is the answer "25"? (truth yes, model no)
- t239: What were the original names of the first three ships in the Sea Organization associated with the Church of Scientology? Is the answer "Avon River, Enchanter, and HMS Royal Scotsman"? (truth yes, model no)
- t250: On what day, month, and year did the 2nd ASEM Transport Ministers' Meeting begin? Is the answer "20 March 2007"? (truth no, model yes)
- t251: Find the contributions of the conductivities of individual ions (ionic equivalent conductance \lambda_+ and \lambda_-) when٨(equivalent ٨ conductance of electrolytic solution) = 0.0412 m^2 /(\Omega) (mol) and t_+ = 0.825.
Is the correct answer "\lambda_+ = 0.0340 m^2 / (Ω) (mol), \lambda_- = 0.0072 m^2 / (Ω) (mol)"? (truth no, model yes)
- t267: A hydraulic press contains $0.25 m^3$ (250 L) of oil. Find the decrease in the volume of the oil when it is subjected to a pressure increase  $\Delta p=1.6 \times 10^7 Pa$ (about 160 atm or 2300 psi). The bulk modulus of the oil is $B=5.0 \times 10^9 Pa$ (about $5.0 \times 10^4 atm$) and its compressibility is $k=1 / B=20 \times 10^{-6} atm^{-1}$. (Unit: 10^{-4} m^3)
Is the correct answer "-0.8"? (truth yes, model no)
- t269: A 120 V dc shunt motor having an armature circuit resistance of 0.2 ohm and a field circuit resistance of 60 ohms, draws a line current of 40 A at full load. The brush volt drop is 3 V and rated, full load speed is 1800 rpm. Calculate: (a) The speed at half load. (b) The speed at an overload of 125 percent.
Is the correct answer "Half-load speed: 1860 rpm, 1(1/4) load speed: 1765 rpm"? (truth yes, model no)
- t274: (1) A 1.5-kw single-phase converter operates at full load from a 230-volt a-c source. Neglecting losses, and assuming a power factor of unity, calculate: (a) the d-c voltage and current; (b) the a-c input current. (2) A 2.5-kw single-phase converter is operated inverted, i.e., it converts direct to alternating current. If the d-c input voltage is 230, calculate: (a) the a-c voltage; (b) the alternating and direct currents at full load.
Is the correct answer "1(a) d-c voltage = 325 volts, d-c current = 4.62 amp; 1(b) a-c input current = 6.25 amp; 2(a) a-c voltage = 162.5 volts; 2(b) alternating current = 15.4 amp, direct current = 10.9 amp"? (truth yes, model no)
- t279: In what key was "I Offer My Life" by Don Moen composed? Is the answer "F Major"? (truth yes, model no)
- t294: Suppose you discovered a new species of bioluminescent worm . How could you prove that it was the worm itself and not some contaminating bacteria that was producing the light ?
Is the correct answer "Place the light-producing substance in complete growth media or physically examine the light-emitting substance under a microscope."? (truth yes, model no)
- t302: A projector for 1 inch × 1 inch lantern slides uses a projector lamp with a circular filament 0.25 inch in diameter. The condensing lens, of focal length 1 inch, forms an image of the filament which just fills a projection lens 1.25 inches in diameter, (a) Find the focal length of the projection lens. (b) How large an image of the slide will the projector produce on a screen located 25.5 ft from the slide? (c) What would be the effect on the image on the screen if half of the projection lens were covered by an opaque card?
Is the correct answer "f = + 5", image of a slide would be 60 inches × 60 inches, a complete image, half as bright, would be seen"? (truth no, model yes)
- t303: Two atoms of scandium are to combine with three atoms of oxygen. If you start with 1 gram of scandium, how much oxygen is required? Scandium has an atomic weight of 44.96 g/mole. The at. wt. of oxygen is 15.999 g/mole.
Is the correct answer ".533 g of oxygen"? (truth yes, model no)
- t312: Jackie Ormes was the arts editor for the Monongahela High School yearbook during which academic year? Is the answer "1929–1930"? (truth yes, model no)
- t315: Air flows through a pipe 5 ft. long with an internal diameter of 0.5 in. The air is flowing at a uniform speed of 80 ft/sec. The wall surface temperature is maintained at 210°F. If air enters at a temperature of 60°F and at atmospheric pressure, calculate the coefficient of heat transfer.
Is the correct answer "18.6 Btu/hr-ft^2-°F"? (truth yes, model no)
- t317: What day, month, and year did Masaki Tsuji win a Special Award in the 13th Animation Kobe for his writing work? Is the answer "September 24, 2008"? (truth yes, model no)
- t320: What's the name of Section 5 of the paper 'Identifying semantic role clusters and alignment types via microrole coexpression tendencies'? Is the answer "Clustering roles"? (truth yes, model no)
- t323: What did Daemon Targaryen say to Rhaenyra about living life in fear in Episode 4, Season 1 of House of the Dragon? Is the answer "You cannot live your life in fear, or you will forsake the best parts of it."? (truth yes, model no)
- t339: A closed system contains pure ammonia (NH_3) at an initial pressure and temperature of 1640psiaand 1460°R respectively. The ammonia then undergoes an isothermal expansion to a final pressure of 820psia. Using the generalized enthalpy correction chart calculate the change in specific enthalpy.
Is the correct answer "13.73 Btu/lbm"? (truth yes, model no)
- t345: What was the year when Cléo Hamon began learning to skate? Is the answer "2006"? (truth yes, model no)
- t346: During what year did Julie Mehretu first marry Jessica Rankin? Is the answer "2008"? (truth yes, model no)
- t350: Who formed the Dubai-based band Sho? in June 2009? Is the answer "Zara Quiroga and Rizal Khan"? (truth yes, model no)
- t357: What was the date, month, and year when Clifford Cunnell, an English cricketer, died? Is the answer "5 October 2016"? (truth yes, model no)
- t360: In which month and year did Thomas le Bonniec reveal himself as the whistleblower and send a letter to European data protection regulators, calling on them to investigate Apple's "past and present" use of Siri recordings? Is the answer "May 2020"? (truth yes, model no)
- t362: How many Big East Championships did Frank Beamer win? Is the answer "3"? (truth yes, model no)
- t363: Who won the first football game between Emory and Henry College and Virginia Tech? Is the answer "Emory & Henry College"? (truth yes, model no)
- t368: Who won the Paris Kanellakis Theory and Practice Award in 2010? Is the answer "Kurt Mehlhorn"? (truth yes, model no)
- t381: What was the year when Vikram S. Buddhi was sentenced to prison? Is the answer "2007"? (truth yes, model no)
- t389: A shaft distributes mechanical power of 160 hp at a speed of 400 rpm. It is subjected to sudden loading and heavy shock conditions with a maximum bending moment of 32,000 lbs-in. Assuming that the shaft has a keyway and considering the ASME code, calculate the suitable diameter for the shaft.
Is the correct answer "4 3/8 in."? (truth yes, model no)
- t397: How old was Fatima Sydow, the famous Cape Malay chef, when she passed away? Is the answer "50."? (truth yes, model no)
- t421: What is the distance between two Cs atoms in a unit cell, if a = 4.5°A?
Is the correct answer "7.790A"? (truth yes, model no)
- t432: Use the van der Waals parameters for chlorine to calculate approximate values of the radius of a $\mathrm{Cl}_2$ molecule regarded as a sphere.
Is the correct answer "0.139$\mathrm{nm}$"? (truth yes, model no)
- t434: Who was awarded the Romer-Simpson Medal in 1997? Is the answer "Colin Patterson"? (truth yes, model no)
- t437: How many summer pasture sites, with 5% sampling intensity, were selected from the study area for the article "The local medicinal plant knowledge in Kashmir Western Himalaya: A way to foster ecological transition via community-centered health-seeking strategies"? Is the answer "Eighteen summer pasture sights."? (truth yes, model no)
- t439: In what episode and season of Scandal did Olivia find out that her mother is a terrorist? Is the answer "Season 3 Episode 9"? (truth yes, model no)
- t444: A biology student from Nebraska, vacationing at a Virginia beach, observes that the level of activity of a fiddler crab changes with the cycle of the tides. When he brings some crabs back with him to Nebraska, he notices that a similar activity cycle is shown, yet there are no ocean beaches for miles. Explain.
Is the correct answer "The crab's activity cycle is determined by the moon's gravitational pull"? (truth yes, model no)
- t456: Find K_b andpK_bfor the acetate ion CH_3COO^-, The ionization constant of CH_3COOH is K_a = 1.75 × 10^-5;K_w= 1.00 × 10^-14.
Is the correct answer "K_b = 5.71 × 10^-10, pK_b = 9.244"? (truth yes, model no)
- t459: A silicious rock contains the mineral ZnS. To analyze for Zn, a sample of the rock is pulverized and treated with HCl to dissolve the ZnS (silicious matter is insoluable). Zinc is precipitated from solution by the addition of potassium ferrocyanide K_4 Fe (CN)_6. After filtering, the precipitate is dried and weighed. The reactions which occur are ZnS + 2HCl \rightarrow ZnCl_2 + H_2 S 2ZnCl_2 + K_4 Fe (CN)_6 \rightarrow Zn_2 Fe (CN)_6 + 4 KCl If a 2 gram sample of rock yields 0.969 gram of Zn_2Fe(CN)_6, what is the percentage of Zn in the sample? Atomic weight Zn = 65.4, molecular weight Zn_2 Fe (CN)_6 = 342.6.
Is the correct answer "18 % Zn"? (truth yes, model no)
- t461: An inexperienced nurse measures the blood pressure in the artery of the upper arm of a man. She then measures the blood pressure in the artery of the man's leg. The nurse obtains a different value. Why?
Is the correct answer "The blood pressure decreases as the blood moves further away from the heart"? (truth yes, model no)
- t465: Distinguish betweenapoenzymesandcofactors .
Is the correct answer "Apoenzymes are the protein constituent of some enzymes and cannot perform enzymatic functions without their respective cofactors, which are smaller non-protein portions. Cofactors can perform enzymatic reactions without an apoenzyme, although at a slower rate."? (truth yes, model no)
- t475: The surface temperature of a 3 ft square panel is maintained at200°F. Calculate the heat lost by the panel (a)whenattached to the ceiling, facing downwards in a room at80°F, and (b)whenattached to the floor, facing upwards in the same room. The condition through the back of the panel may be neglected. Take \epsilon = 0.9 for the panel surface.
Is the correct answer "197.7 Btu/hr.ft.^2 and 300.5 Btu/hr.ft^2"? (truth yes, model no)
- t479: A square wave guide of side 2b and a circular wave guide of diameter2d have the same cross-sections. If the cutoff wavelength of the square guide is 4b, find the cutoff wave lengthof the circular wave guide.
Is the correct answer "1.77d"? (truth yes, model no)
- t482: What place did the album "Rolling Papers 2" by Wiz Khalifa receive on the 2018 US Billboard 200 year-end charts? Is the answer "128th"? (truth yes, model no)
- t485: As the life of a star progresses heavy elements are produced. The elements form layers around the star in this order (starting from the outer layer):
Is the correct answer "H → He → C → O → Ne → Si → Fe"? (truth yes, model no)
- t493: Before the New 52, who was responsible for Rainbow Raider's death? Is the answer "Blacksmith"? (truth yes, model no)
- t511: For which province of Pakistan was Ghulam Ishaq Khan (former Governor of the State Bank of Pakistan) appointed as the Home Secretary in the year 1956? Is the answer "Sindh."? (truth yes, model no)
- t515: The drag of a ship in water is assumed to depend on the Reynolds number and the Froude number so that [drag / {(1/2)(\rhoV^2A)}] = f [{(\rhoVD) / \mu}, (V^2 / gD)] It is proposed that a model one-tenth the size of a full-scale ship be tested in water and the results be used to predict the performance of the full-scale ship. Is this feasible?
Is the correct answer "the attainment of dynamic similarity in model and prototype is not possible"? (truth yes, model no)
- t527: In which episode and season of South Park does Bill Cosby (BSM-471) first appear? Give me the number and title. Is the answer "Season 4 Episode 12: "Trapper Keeper""? (truth yes, model no)
- t533: Two masses m_1 = 5 kg and m_2 = 10 kg have velocities u^\ding{217}_1= 2m/sec in the +x direction and u^\ding{217}_2= 4 m/sec in the +y direction. They collide and stick together. What is their final velocity after collision?
Is the correct answer "2.750 m/sec"? (truth yes, model no)
- t536: On what month, date, and year did the Southern Baptist Convention meet for their annual convention, approve a resolution condemning sexual abuse, and establish a special committee to investigate sexual abuse? Is the answer "June 12 2019"? (truth yes, model no)
- t539: \rho/P, g/liter-atm 10 11 10 (\rho = density) P,atm: 1 10 20 The critical pressure of this gas must then be (greater than 10atm, greater than 20atm, between 1 and 20atm, between 1 and 10atm, less than 20atm, can't tell).
Is the correct answer "cannot be determined without additional information"? (truth no, model yes)
- t542: As of 6 April 2022, how many Hillsong branches in the U.S. had separated from the church since the revelations about Brian Houston? Is the answer "9"? (truth yes, model no)
- t545: In what year did Donald Arthur Norman receive the Franklin Institute Awards (Benjamin Franklin Medal)? Is the answer "2008"? (truth no, model yes)
- t546: Who was the 9th Chief Minister of Jammu and Kashmir? Is the answer "Mehbooba Mufti"? (truth yes, model no)
- t548: Calculate the standard potential of the $\mathrm{Ce}^{4+} / \mathrm{Ce}$ couple from the values for the $\mathrm{Ce}^{3+} / \mathrm{Ce}$ and $\mathrm{Ce}^{4+} / \mathrm{Ce}^{3+}$ couples.
Is the correct answer "-1.46 $\mathrm{V}$"? (truth yes, model no)
- t564: During his education days, the 13th Chief Justice of India, S. M. Sikri, moved to London to initially study which subject but later switched to law, studying at Trinity College, Cambridge? Is the answer "medicine"? (truth yes, model no)
- t579: What is the value assigned to the 'k' argument in the Partitioning Around Medoids algorithm in the right-side plot of Figure 9 in the paper "Generating Semantic Maps through Multidimensional Scaling: Linguistic Applications and Theory"? Is the answer "5"? (truth yes, model no)
- t590: In which year did Clive Derby-Lewis become deputy mayor of Bedfordview? Is the answer "1973"? (truth yes, model no)
- t593: A 3.5 ft. mean diameter cast-iron flywheel, rotating at 250 rpm, can furnish 750 ft.-lb. of energy for a small rock crushing operation. Calculate the thickness of the flywheel rim if the width is kept to a minimum of 5 in. The speed variation is not to exceed 19% for the crushing operation. Specific weight of cast-iron is 0.26 lbs./in^3.
Is the correct answer "1 in."? (truth yes, model no)
- t598: If the speed of an airplane is measured by means of a stagnation tube, what correction must be applied to the constant-density indication when the plane is cruising at 300 mph?
Is the correct answer "- 5 mph"? (truth yes, model no)
- t599: What is the cost of operating for 24 hr a lamp requiring1.0 amp on a 100-volt line if the cost of electric energy is $0.50/kw-hr?
Is the correct answer "$0.12"? (truth yes, model no)
- t601: Other than being a choreographer for the TV series In Living Color, what other job did Rosie Perez do on the show? Is the answer "segment producer"? (truth yes, model no)
- t613: Water film boiling occurs on top of a horizontal plate. The wateris at a pressure of 1 atm. and the surface temperature ofthe plate is 554°C. Calculate the heat flux given off by waterassuming a characteristic length (L_c) of 1 cm.
Is the correct answer "59,830 W/m^2 or 5.983 W/cm^2"? (truth yes, model no)
- t614: In 2009, what was the seating capacity of Dragão Arena (Dragão Caixa)? Is the answer "2,179"? (truth yes, model no)
- t616: A 2-liter Dumas bulb contains n moles of nitrogen at 0.5atm pressure and at T°K. On addition of 0.01 moles of oxygen, it is necessary to cool the bulb to a temperature of 10°C in order to maintain the same pressure. Calculate n and T.
Is the correct answer "n = 0.0332, T = 367K"? (truth yes, model no)
- t623: Calculate the equilibrium mixture of the carbon monoxide combustionreaction at 2504°C and 1atmpressure. Assume that the CO reacts with astoichiometricamount ofair and thatK_pfor the reaction is equal to 49.365.
Is the correct answer "y = 0.368"? (truth yes, model no)
- t628: What is the impedance of a circuit if 100\angle0° V causes a current7.07 + j7.07 A?
Is the correct answer "8.2 - j5.7 Ω"? (truth yes, model no)
- t632: What will be the final concentration of a solution of 50 ml of .5M H_2SO_4 added to 75 ml of .25M H_2SO_4 (the final volume is 125 ml)?
Is the correct answer "35 M H_2SO_4"? (truth yes, model no)
- t634: In what creature were Gabriel's memories stored during Good Omens Season 2? Is the answer "Woofles"? (truth no, model yes)
- t646: An electron is separated from a proton by a dis-tance of 10^\rule{1em}{1pt}10 m. What is the gravitational and electro-static potential energy due to the proton at the position of the electron? How much work is required against each field to move the electron to a position of separation 5 × 10^\rule{1em}{1pt}10 m?
Is the correct answer "W_G = 8.1 × 10^58 J, W_E = 1.84 × 10^18 J"? (truth yes, model no)
- t647: What year was the municipality of San Pedro de Urabá, Antioquia, Colombia, founded? Is the answer "1835"? (truth no, model yes)
- t648: A wine has an acetic acid (CH_3 COOH, 60 g/formula weight) content of 0.66% by weight. If the density of the wine is 1.11 g/ml, what is the formality of the acid?
Is the correct answer "1.2 × 10^-3 F"? (truth yes, model no)
- t654: Two long, charged, thin-walled, concentric cylindrical shells have radii of 3.0 and $6.0 \mathrm{~cm}$. The charge per unit length is $5.0 \times 10^{-6} \mathrm{C} / \mathrm{m}$ on the inner shell and $-7.0 \times 10^{-6} \mathrm{C} / \mathrm{m}$ on the outer shell. What is the magnitude $E$ of the electric field at radial distance $r=4.0 \mathrm{~cm}$?
Is the correct answer "$2.3$$10^6 \mathrm{~N} / \mathrm{C} $"? (truth yes, model no)
- t657: From which university did Sergio Fajardo Valderrama receive his M.Sc. in Mathematics? Is the answer "Universidad de los Andes"? (truth yes, model no)
- t659: A zincmineral slurry consists of ore particles and water in thevolumetric ratio of 1 : 3. The volumetric ratio of zinc mineral(sp. gr. = 3.8) to ore particles (sp. gr. = 2.6) is 0.2. The mineral particles are 0.007 in. in diameter. If the particlesof zinc mineral are settling under gravity, determine theterminal velocity of the particles. Take viscosity of water as\mu = 8.1 × 10^-4 lb/ft-s.
Is the correct answer "0.039 ft/s"? (truth yes, model no)
- t663: In which year was Richard Day first elected as a Republican? Is the answer "1990"? (truth yes, model no)
- t675: In what month did the New Zealand authorities officially end the search for the vintage yacht Niña, which disappeared while traveling across the Tasman Sea in 2013? Is the answer "July"? (truth yes, model no)
- t688: Air flows in a sheet-metal ventilation duct having a cross-sectionalarea of 6 ft^2 at a velocity of 40 fps. If a butterflytype of control were suddenly closed, what initial forcewould be exerted upon it ?
Is the correct answer "1320 lb"? (truth yes, model no)
- t702: Which ward in Tokyo was the AT-1 phono cartridge created in? Is the answer "Shinjuku"? (truth yes, model no)
- t710: What were the day, month, and year of the Aseprite v1.3-beta1 release? Is the answer "4 Dec 2020"? (truth no, model yes)
- t713: You have collected a tissue specimen that you would like to preserve by freeze drying. To ensure the integrity of the specimen, the temperature should not exceed $-5.00{ }^{\circ} \mathrm{C}$. The vapor pressure of ice at $273.16 \mathrm{~K}$ is $624 \mathrm{~Pa}$. What is the maximum pressure at which the freeze drying can be carried out?
Is the correct answer "425 $\mathrm{~Pa}$"? (truth yes, model no)
- t715: In what city and state is Richard Neutra's Slavin House located? Is the answer "Santa Barbara, California"? (truth yes, model no)
- t716: Carbon dioxide is assumed to follow the equation of state [P + {n / (V^2T^(1/2))}] (v - m) = RT where n and m are constants for any gas. Given that the critical pressure and temperature of carbon dioxide are 72.9atmand 304.2°K respectively, determine the compressibility factor of the gas at 100°C and at a volume of 6.948 cubic decimeters per kilogram.
Is the correct answer "0.8155"? (truth no, model yes)
- t717: A saturated solution of CaF_2 contains .00168g of CaF_2 per 100g of water. Determine theK_sp.
Is the correct answer "3.92 × 10^-8"? (truth yes, model no)
- t727: In what year was the De Gennes Prize (formerly known as the Prize for Materials Chemistry) established? Is the answer "2006"? (truth no, model yes)
- t730: What month and year was the album "Introspective" released by Inner Ear Records? Is the answer "June 4, 2021"? (truth yes, model no)
- t737: Cerenkov radiation can be loosely compared to the shock wave caused by a speed boat traveling in shallow water. If the boat moves at 60 km/hr and if the bow wave has an apex angle of 30°, what is h, the depth of the water? [Phase velocity of water wavesv_ph= \surd(gh)]
Is the correct answer "7m"? (truth yes, model no)
- t740: What are the four keywords of the paper "New Avenues and Challenges in Semantic Map Research"? Is the answer "semantic maps, inference, graph, emotions"? (truth yes, model no)
- t742: Who was the first visual artist to be awarded the Peace Prize of the German Book Trade? Is the answer "Anselm Kiefer"? (truth yes, model no)
- t748: Do $\mathrm{HF} / 6-31 \mathrm{G}^*$ geometry optimizations on one conformers of $\mathrm{HCOOH}$ with $\mathrm{OCOH}$ dihedral angle of $0^{\circ}$. Calculate the dipole moment.
Is the correct answer "1.41 $\mathrm{D}$"? (truth yes, model no)
- t755: How far (in km) is Karbala from Baghdad? Is the answer "88 kilometers"? (truth yes, model no)
- t758: A parallel beam of light of radiant energy density 6.4 × 10^4 J/m^3 is incident on a plane mirror. What is a) the momentum acting upon the mirror and b) the force exerted upon it during 5 seconds illumination?
Is the correct answer "4.28 × 10^-4kgm/s, 8.58 × 10^-5 N/m^2"? (truth yes, model no)
- t760: In the online game World of Warcraft, in patch 5.2.0, what change was made to the cooldown of the shaman ability Elemental Mastery? Is the answer "Decreased to 90 seconds"? (truth yes, model no)
- t765: The potential energy of a compressed spring and the potential energy of a charged object both depend on
Is the correct answer "the work done on them"? (truth yes, model no)
- t766: Compute the heat gained by the room at 80°F from a vertical plate3 ft. wide and 4 ft. high maintained at 115°F.
Is the correct answer "596.4 Btu/hr"? (truth yes, model no)
- t767: On Feb. 12, 2018, in what city was Dua Lipa performing when she raised a rainbow flag? Is the answer "Los Angeles"? (truth yes, model no)
- t771: On what date (Month/Day/Year) were two ancient cannons presented to Plymouth at Burial Hill by the British Government? Is the answer "20 April 1931"? (truth no, model yes)
- t772: You are given .01 moles ofAgCl. Assuming theKeqfor Ag(NH_3 )_2 is 1.74 × 10^7 , how much 1M ammonia solution is required to dissolve thisAgCl? Assume, also,K_spofAgClis 2.8 × 10^-10 .
Is the correct answer "154 ml"? (truth yes, model no)
- t777: On what day, month, and year did Taiwanese conductor and violinist Felix Chen die? Is the answer "August 16, 2008"? (truth no, model yes)
- t780: In what year did Patty Berg become the first woman to hit a hole-in-one during a USGA competition at the U.S. Women's Open? Is the answer "1959"? (truth yes, model no)
- t784: 2NaHCO_3(s) \rightarrow Na_2CO_3(s) \rightarrow CO_2 (g) + H_2O(l) , ∆H = 30.92 Kcal/mole. ∆H°_Na2 CO3 _(s) = - 270.3. ∆H°CO2 (g)= - 94.0 and ∆H°H2 O_(l) = - 68.4 Kcal/mole, what is the standard enthalpy of formation for NaHCO3(s)?
Is the correct answer "- 220.0 Kcal/mole"? (truth yes, model no)
- t790: What day, month, and year did over 500,000 people gather at the Black Star Square in Ghana to welcome former U.S. President Bill Clinton and his wife, Hillary Clinton? Is the answer "March 24, 1998"? (truth yes, model no)
- t799: What year was John Monteath Robertson awarded the Gregori Aminoff Prize? Is the answer "1983"? (truth yes, model no)
- t801: What year was the municipality of Santo Domingo, Antioquia, Colombia, founded? Is the answer "1778"? (truth yes, model no)
- t804: The refractive powers of the front and back lenses of a Galilean-type telescope are + 10.00dioptersand - 12.50 dioptersrespectively. What must the separation of the two lenses be if the system is to beafocal? What is the angular magnification?
Is the correct answer "2cm, -1.25"? (truth yes, model no)
- t814: What is the surname of the individual who was awarded the Geoffrey Barker Medal in 2020? Is the answer "MacPherson"? (truth yes, model no)
- t821: A stream of air is flowing over a flat plate with a velocity of 33 ft/sec, at atmospheric pressure and 60°F. Calculate the boundary layer thickness on the plate at 4 in. from the leading edge.
Is the correct answer "0.0708 in"? (truth yes, model no)
- t823: Name the bowed instrument played in Kashmir? Is the answer "Saz-e-Kashmir"? (truth yes, model no)
- t829: Before the New 52, who murdered the supervillain Monsieur Mallah? Is the answer "Gorilla Grodd"? (truth yes, model no)
- t835: Ribonuclease has a partial specific volume of (0.707 cm^3 g^-1) and diffusion coefficient of (13.1 × 10^-7 cm^2 sec^-1) cor-rected to water at 20°C. The density of water at 20°C is 0.998 (g/cm^3). Calculate the molecular weight of ribonuclease using the Svedberg equation. Assume that the sedimentation coefficient for ribonuclease is 2.02 × 10^-13 sec.
Is the correct answer "13,000 g/mole"? (truth yes, model no)
- t836: Find the magnitude of E for a plane wave in free space, if the magnitude of H for this wave is 5 amp/meter.
Is the correct answer "1883 volts/meter"? (truth yes, model no)
- t841: Air at 170°F is transported through a rectangular duct 3 in. high and 6 in. wide. The duct is 18 ft. long, and the walls are maintained at a temperature of 65°F. As-suming an air flow of 25 lbm/hr, determine the bulk mean temperature of the air as it leaves the duct.
Is the correct answer "128°F"? (truth yes, model no)
- t856: What are the first, middle, and last names of the first Speaker of the West Pakistan Legislative Assembly? Is the answer "Fazal Ilahi Chaudhry"? (truth yes, model no)
- t860: Find the steady-state solution of the equation y [n] + [1 / \surd(3)]y [n - 1] =cos(\pi/6) n.
Is the correct answer "y_ss[n] = \surd(3/7)cos[(\pi/6)n tan^-1 [{1} / {3\surd(3)}]"? (truth yes, model no)
- t865: In a continuously fed catalytic ammonia converter 1 mol of nitrogenreacts with 3 mol of hydrogen according to the followingchemical reaction: N_2 + 3H_2 = 2NH_3 The converter is operated at a pressure of 100atmand a temperatureof 350°C. The equilibrium constant for this reactionK is equal to 14.4 × 10^-5 at 500°C. The enthalpy of reaction\DeltaH^0 is - 25,800 cal/g-mol at the desired temperatures. All standard states are assumed to be pure componentsat 1atmpressure. Assume ideal-gas and Lewis-Randall behavior.Calculate the equilibrium conversionof nitrogen to ammonia.
Is the correct answer "54% conversion"? (truth yes, model no)
- t866: Air flows through a pipe, and cooling is achieved by means of forced convection. Air flowing at a speed of 100 ft/sec enters the pipe at a temperature and pressure of 68°F and 14.2 psi, respectively. The pipe is 3 ft. in length, with a 0.8 in. diameter. The wall surface temperature is 200°F. If the pressure drop over the length is 3.2 in. of water, calculate the heat transferred from the pipe to the air.
Is the correct answer "1571.56 Btu/hr"? (truth yes, model no)
- t875: What will be the final concentration of I^- in a solution made by mixing 35.0 ml of 0.100 M NaHSO_3 with 10.0 ml of 0.100 M KIO_3? Assume volumes are additive.
Is the correct answer "1.0 ×10^-3 moles"? (truth yes, model no)
- t877: Which of Smith Wigglesworth's grandchildren became the president of Elim Pentecostal Church? Is the answer "Neil Sloane"? (truth no, model yes)
- t896: As of 2022, what character (first and last name) was Dog's original owner on The Walking Dead TV series? Is the answer "Leah Shaw"? (truth yes, model no)
- t899: In what subject did photographer Kemka Ajoku attain a bachelor's degree in 2020? Is the answer "Mechanical Engineering"? (truth yes, model no)
- t903: Using the Bohr formula, calculate the wave numbers of the first five members of the spectrum emitted by ionized helium.
Is the correct answer "9877.56, 15243.17, 18478.43, 20578.25, 22017.88"? (truth yes, model no)
- t919: What is the weight of the Puzzling Stone Sword from Dark Souls II in in-game units? Is the answer "2"? (truth yes, model no)
- t925: On August 2, 2017, the Supreme Court of India sentenced Neera Yadav, a former officer of the Indian Administrative Service (IAS), to how many years of imprisonment in the Noida land allotment scam? Is the answer "2"? (truth yes, model no)
- t932: What was John Graham Lough's cause of death? Is the answer "Pneumonia"? (truth yes, model no)
- t933: When 100 g of water at 0°C are mixed with 50 g of water at 50°C, what is the change of entropy on mixing?
Is the correct answer "0.5 cal/K/deg"? (truth yes, model no)
- t940: In which episode of Season 5 does the British period drama Downton Abbey refer to the Jallianwala Bagh massacre? Is the answer "3"? (truth no, model yes)
- t941: 10 cc of battery acid (density 1.21) is diluted to 100 cc. 30 cc of the dilute solution is neutralized by 45 cc of 0.5 N base. What is the normality of the diluted acid? What is its strength in grams per liter? What is the strength of the undiluted 1.21 density acid in g/l?
Is the correct answer "0.75 N, 121 g/l, 1210 g/l"? (truth yes, model no)
- t943: What flowers were shown in artist J.C. Leyendecker's May 30, 1914, "The Saturday Evening Post" cover? Is the answer "Hyacinths"? (truth yes, model no)
- t944: What are the day, month, and year of birth of the linguist William Croft? Is the answer "November 13, 1956"? (truth yes, model no)
- t950: Given the reaction A + B \rightleftarrows C + D, find the equilibrium constant for this reaction if .7 moles of C are formed when 1 mole of A and 1 mole of B are initially present. For this same equilibrium, find the equilibrium composition when 1 mole each of A, B, C, and D are initial-ly present.
Is the correct answer "equilibrium constant is 5.44, concentration of A and B is 0.6M, and of C and D is 1.4M"? (truth yes, model no)
- t954: The wet-bulb thermometer reads a temperature of 65°F whenair at atmospheric pressure and 95°F blows across the thermometer. Determine the relative humidity of the air stream.
Is the correct answer "21.7 %"? (truth yes, model no)
- t965: A signal source operating at 50MHz has an output impedance of 20 ohms. It is to supply power through a coaxial line to a load impedance of 150 + j40 ohms. Is it possible to design a quarter-wave transformer to match the source to the load?
Is the correct answer "The matching transformer would need a characteristic impedance = √[(20)(150)] = 54.77 ohms"? (truth no, model yes)
- t972: What is the distance (in km) between the city of Udhampur and the Krimchi Temples in Jammu? Is the answer "12"? (truth yes, model no)
- t977: What year was the municipality of Sativasur, Boyacá, Colombia, founded? Is the answer "1720"? (truth yes, model no)
- t983: How heavy is my Ricoh GR III body only in grams? Is the answer "227 grams"? (truth yes, model no)
- t990: Find the system function H(j\omega) = [{V_i (j\omega)} / {I_i (j\omega)}], and impulse response of a one-port network if the input voltage, v_i(t) = 100cos\omega_ot V, produces the input current, I_i (j\omega) = 100\pi [\delta (\omega +\omega_o) + \delta(\omega -\omega_o)] [(1 - j) / 2\omega].
Is the correct answer "h(t) = \delta(t) - (1 / 2) e^-(1/2)t"? (truth yes, model no)
- t999: The rating of a certain machine from the name-plate is 110 volts, 38.5 amperes, 5h.p. Find the input, output and efficiency at full load.
Is the correct answer "Input: 4350 watts, Output: 3730 watts, Efficiency: 85.7 percent"? (truth yes, model no)
