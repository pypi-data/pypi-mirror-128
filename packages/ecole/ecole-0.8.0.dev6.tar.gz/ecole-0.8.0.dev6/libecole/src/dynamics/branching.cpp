#include <algorithm>
#include <stdexcept>

#include <fmt/format.h>
#include <xtensor/xtensor.hpp>

#include "ecole/dynamics/branching.hpp"
#include "ecole/scip/model.hpp"
#include "ecole/scip/utils.hpp"

namespace ecole::dynamics {

BranchingDynamics::BranchingDynamics(bool pseudo_candidates_) noexcept : pseudo_candidates(pseudo_candidates_) {}

namespace {

std::optional<xt::xtensor<std::size_t, 1>> action_set(scip::Model const& model, bool pseudo) {
	if (model.stage() != SCIP_STAGE_SOLVING) {
		return {};
	}
	auto const branch_cands = pseudo ? model.pseudo_branch_cands() : model.lp_branch_cands();
	auto branch_cols = xt::xtensor<std::size_t, 1>::from_shape({branch_cands.size()});
	auto const var_to_idx = [](auto const var) { return SCIPvarGetProbindex(var); };
	std::transform(branch_cands.begin(), branch_cands.end(), branch_cols.begin(), var_to_idx);

	assert(branch_cols.size() > 0);
	return branch_cols;
}

}  // namespace

auto BranchingDynamics::reset_dynamics(scip::Model& model) -> std::tuple<bool, ActionSet> {
	model.solve_iter_start_branch();
	if (model.solve_iter_is_done()) {
		return {true, {}};
	}
	return {false, action_set(model, pseudo_candidates)};
}

auto BranchingDynamics::step_dynamics(scip::Model& model, std::size_t const& var_idx) -> std::tuple<bool, ActionSet> {
	auto const vars = model.variables();
	if (var_idx >= vars.size()) {
		throw std::invalid_argument{
			fmt::format("Branching candidate index {} larger than the number of variables ({}).", var_idx, vars.size())};
	}
	scip::call(SCIPbranchVar, model.get_scip_ptr(), vars[var_idx], nullptr, nullptr, nullptr);
	model.solve_iter_branch(SCIP_BRANCHED);

	if (model.solve_iter_is_done()) {
		return {true, {}};
	}
	return {false, action_set(model, pseudo_candidates)};
}

}  // namespace ecole::dynamics
