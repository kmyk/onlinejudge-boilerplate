#include <bits/stdc++.h>
#define REP(i, n) for (int i = 0; (i) < (int)(n); ++ (i))
#define REP3(i, m, n) for (int i = (m); (i) < (int)(n); ++ (i))
#define REP_R(i, n) for (int i = (int)(n) - 1; (i) >= 0; -- (i))
#define REP3R(i, m, n) for (int i = (int)(n) - 1; (i) >= (int)(m); -- (i))
#define ALL(x) begin(x), end(x)
using ll = long long;
using namespace std;
{% if mod %}
const long long MOD = {{ mod }};
{% endif %}
{% if yes_str %}
const string YES = "{{ yes_str }}";
{% endif %}
{% if no_str %}
const string NO = "{{ no_str }}";
{% endif %}

{% if prediction_success %}
void solve({{ formal_arguments }}) {
    cout << "Hello, world!" << endl;
}
{% endif %}

int main() {
    {% if prediction_success %}
    bool test_samples = false;
    if (not test_sample) {
        {{input_part}}
        solve({{ actual_arguments }});
    } else {
        const char *samples[] = {
            ((SAMPLES))
        };
        REP (i, std::distance(ALL(samples))) {
            cerr << "[*] sample " << i << endl;
            istringstream iss(samples[i]);
            ((SAMPLE_INPUT_PART)){{input_part}}
            solve({{ actual_arguments }});
        }
    }
    {% else %}
    // failed to predict input format
    {% endif %}
    return 0;
}
