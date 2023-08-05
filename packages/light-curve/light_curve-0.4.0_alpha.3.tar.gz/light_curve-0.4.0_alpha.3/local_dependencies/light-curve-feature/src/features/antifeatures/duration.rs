use crate::evaluator::*;

macro_const! {
    const DOC: &str = r#"
Time-series duration

$$
t_{N-1} - t_0.
$$

- Depends on: **time**
- Minimum number of observations: **1**
- Number of features: **1**
"#;
}

#[doc = DOC!()]
#[derive(Clone, Default, Debug, Deserialize, Serialize, JsonSchema)]
pub struct Duration {}

impl Duration {
    pub fn new() -> Self {
        Self {}
    }

    pub fn doc() -> &'static str {
        DOC
    }
}

lazy_info!(
    DURATION_INFO,
    size: 1,
    min_ts_length: 1,
    t_required: true,
    m_required: false,
    w_required: false,
    sorting_required: true,
);

impl<T> FeatureEvaluator<T> for Duration
where
    T: Float,
{
    fn eval(&self, ts: &mut TimeSeries<T>) -> Result<Vec<T>, EvaluatorError> {
        self.check_ts_length(ts)?;
        Ok(vec![ts.t.sample[ts.lenu() - 1] - ts.t.sample[0]])
    }

    fn get_info(&self) -> &EvaluatorInfo {
        &DURATION_INFO
    }

    fn get_names(&self) -> Vec<&str> {
        vec!["ANTIFEATURE_duration"]
    }

    fn get_descriptions(&self) -> Vec<&str> {
        vec!["time-series duration"]
    }
}

#[cfg(test)]
#[allow(clippy::unreadable_literal)]
#[allow(clippy::excessive_precision)]
mod tests {
    use super::*;
    use crate::tests::*;

    check_feature!(Duration);

    feature_test!(
        duration,
        [Duration::new()],
        [4.0],
        [0.0_f32, 1.0, 2.0, 3.0, 4.0],
    );
}
